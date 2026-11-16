-- Orchid mGBA bridge (mGBA 0.10+ scripting API)
-- Load in mGBA: Tools > Scripting... > File > Load script... > this file.
-- Listens on 127.0.0.1:8888 (or next free port) for newline-delimited commands.
-- Each command gets exactly one reply line: "ok [...]" or "err <reason>".
--
-- Commands:
--   press <KEYS> [hold=6] [gap=6]   tap keys (e.g. A, B, UP, A+UP), then release for gap frames
--   hold <KEYS> <frames>            hold keys for N frames
--   wait <frames>                   advance N frames with no input
--   shot <path>                     save a PNG screenshot of the current frame
--   read8|read16|read32 <addr>      read memory (hex or decimal address)
--   readrange <addr> <len>          read bytes, reply as hex
--   write8|write16|write32 <addr> <value>
--   savestate <path> | loadstate <path>
--   frame                           current frame counter
--   reset                           reset the core
--   loadrom <path>                  load a (rebuilt) ROM into the core and reset
--   ping

local KEYS = {
	A = C.GBA_KEY.A, B = C.GBA_KEY.B, SELECT = C.GBA_KEY.SELECT, START = C.GBA_KEY.START,
	RIGHT = C.GBA_KEY.RIGHT, LEFT = C.GBA_KEY.LEFT, UP = C.GBA_KEY.UP, DOWN = C.GBA_KEY.DOWN,
	R = C.GBA_KEY.R, L = C.GBA_KEY.L,
}

local server = nil
local clients = {}
local nextId = 1
local queue = {}     -- pending { id=, line= }
local current = nil  -- active timed command

local function reply(id, msg)
	local sock = clients[id]
	if sock then sock:send(msg .. "\n") end
end

local function parseKeys(spec)
	local mask = 0
	for name in string.gmatch(spec:upper(), "[^+]+") do
		local k = KEYS[name]
		if k == nil then return nil, "unknown key " .. name end
		mask = mask | (1 << k)
	end
	return mask
end

local function num(s)
	if s == nil then return nil end
	return tonumber(s)
end

-- Returns nil if the command completed immediately, or a timed-command table.
local function startCommand(id, line)
	local args = {}
	for w in string.gmatch(line, "%S+") do args[#args + 1] = w end
	local cmd = (args[1] or ""):lower()

	if cmd == "" then return nil end
	if cmd == "ping" then reply(id, "ok pong") return nil end
	if cmd == "frame" then reply(id, "ok " .. emu:currentFrame()) return nil end
	if cmd == "reset" then emu:reset() reply(id, "ok") return nil end
	if cmd == "loadrom" then
		-- loadrom <rom.gba> [save.sav]: load a rebuilt ROM plus a save, then reset.
		-- The save defaults to the ROM path with .sav and is loaded as a temporary
		-- copy, so in-game saving never writes back to the file.
		if not args[2] then reply(id, "err missing path") return nil end
		local okL, res = pcall(function() return emu:loadFile(args[2]) end)
		if not okL or res == false then reply(id, "err loadFile " .. tostring(res)) return nil end
		local sav = args[3] or args[2]:gsub("%.gba$", ".sav")
		local savMsg = "no save"
		local okF, f = pcall(function() return io.open(sav, "rb") end)
		if okF and f then
			f:close()
			local okS, r2 = pcall(function() return emu:loadSaveFile(sav, true) end)
			savMsg = (okS and r2 ~= false) and ("save " .. sav) or ("save failed " .. tostring(r2))
		end
		emu:reset()
		reply(id, "ok " .. savMsg)
		return nil
	end

	if cmd == "press" or cmd == "hold" then
		local mask, e = parseKeys(args[2] or "")
		if not mask then reply(id, "err " .. (e or "missing keys")) return nil end
		local holdN = num(args[3]) or 6
		local gapN = (cmd == "press") and (num(args[4]) or 6) or 0
		return { id = id, keys = mask, hold = holdN, gap = gapN }
	end
	if cmd == "wait" then
		return { id = id, keys = 0, hold = 0, gap = num(args[2]) or 1 }
	end
	if cmd == "shot" then
		if not args[2] then reply(id, "err missing path") return nil end
		emu:screenshot(args[2])
		reply(id, "ok " .. args[2])
		return nil
	end
	if cmd == "read8" or cmd == "read16" or cmd == "read32" then
		local a = num(args[2])
		if not a then reply(id, "err bad address") return nil end
		reply(id, string.format("ok 0x%X", emu[cmd](emu, a)))
		return nil
	end
	if cmd == "write8" or cmd == "write16" or cmd == "write32" then
		local a, v = num(args[2]), num(args[3])
		if not a or not v then reply(id, "err bad address/value") return nil end
		emu[cmd](emu, a, v)
		reply(id, "ok")
		return nil
	end
	if cmd == "readrange" then
		local a, n = num(args[2]), num(args[3])
		if not a or not n then reply(id, "err bad address/len") return nil end
		local bytes = emu:readRange(a, n)
		reply(id, "ok " .. (bytes:gsub(".", function(c) return string.format("%02X", c:byte()) end)))
		return nil
	end
	if cmd == "savestate" then
		local ok = emu:saveStateFile(args[2], C.SAVESTATE.ALL)
		reply(id, ok and "ok" or "err savestate failed")
		return nil
	end
	if cmd == "loadstate" then
		local ok = emu:loadStateFile(args[2], C.SAVESTATE.ALL)
		reply(id, ok and "ok" or "err loadstate failed")
		return nil
	end
	reply(id, "err unknown command " .. cmd)
	return nil
end

local function onFrame()
	-- Start queued commands until one needs frames to elapse.
	while current == nil and #queue > 0 do
		local item = table.remove(queue, 1)
		current = startCommand(item.id, item.line)
	end
	if current == nil then emu:setKeys(0) return end

	if current.hold > 0 then
		emu:setKeys(current.keys)
		current.hold = current.hold - 1
	elseif current.gap > 0 then
		emu:setKeys(0)
		current.gap = current.gap - 1
	end
	if current.hold <= 0 and current.gap <= 0 then
		emu:setKeys(0)
		reply(current.id, "ok")
		current = nil
	end
end

local function onReceived(id)
	local sock = clients[id]
	if not sock then return end
	sock.buf = sock.buf or ""
	while true do
		local p, err = sock:receive(1024)
		if p then
			sock.buf = sock.buf .. p
			while true do
				local nl = sock.buf:find("\n")
				if not nl then break end
				local line = sock.buf:sub(1, nl - 1):gsub("\r", "")
				sock.buf = sock.buf:sub(nl + 1)
				queue[#queue + 1] = { id = id, line = line }
			end
		else
			if err ~= socket.ERRORS.AGAIN then
				clients[id] = nil
				sock:close()
			end
			return
		end
	end
end

local function onAccept()
	local sock, err = server:accept()
	if err then console:error("bridge accept: " .. tostring(err)) return end
	local id = nextId
	nextId = id + 1
	clients[id] = sock
	sock:add("received", function() onReceived(id) end)
	sock:add("error", function() clients[id] = nil sock:close() end)
end

callbacks:add("frame", onFrame)

local port = 8888
while not server do
	local err
	server, err = socket.bind("127.0.0.1", port)
	if err then
		server = nil
		if err == socket.ERRORS.ADDRESS_IN_USE then
			port = port + 1
		else
			console:error("bridge bind: " .. tostring(err))
			break
		end
	else
		local _, lerr = server:listen()
		if lerr then
			console:error("bridge listen: " .. tostring(lerr))
			server:close()
			server = nil
			break
		end
		server:add("received", onAccept)
		console:log("Orchid bridge listening on 127.0.0.1:" .. port)
	end
end
