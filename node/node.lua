node.alias("keyboard")

gl.setup(NATIVE_WIDTH, NATIVE_HEIGHT)

local json = require "json"

util.loaders.json = function(filename)
    return json.decode(resource.load_file(filename))
end

util.resource_loader{
    "data.json",
    "dejavu_sans.ttf"
}

function draw_key(keyboard_options, key_options, x, y, text_upper, text_lower, text_right, text_upper_right)
    local key_size = keyboard_options.keySize
    local num_rows = keyboard_options.numRows
    local row_width = keyboard_options.rowWidth
    local key_width = 1
    if key_options.key_width ~= nil then
        key_width = key_options.key_width
    end
    local screen_x = (WIDTH - key_size * row_width) / 2 + key_size * x
    local screen_y = (HEIGHT - key_size * num_rows) / 2 + key_size * y
    resource.create_colored_texture(1, 1, 1, 1):draw(screen_x + 1, screen_y + 1, screen_x + (key_width * key_size) - 1, screen_y + key_size - 1)
    if key_options.descender then
        resource.create_colored_texture(1, 1, 1, 1):draw(screen_x + key_size * (key_width - 1) + 1, screen_y + key_size - 1, screen_x + (key_width * key_size) - 1, screen_y + (2 * key_size) - 1)
    end
    if text_upper ~= nil then
        dejavu_sans:write(screen_x + 1, screen_y + 1, text_upper, key_size / 2 - 1, 0, 0, 0, 1)
    end
    if text_lower ~= nil then
        dejavu_sans:write(screen_x + 1, screen_y + key_size / 2, text_lower, key_size / 2 - 1, 0, 0, 0, 1)
    end
    if text_right ~= nil then
        dejavu_sans:write(screen_x + key_size / 2, screen_y + key_size / 2, text_right, key_size / 2 - 1, 0, 0, 0, 1)
    end
    if text_upper_right ~= nil then
        dejavu_sans:write(screen_x + key_size / 2, screen_y + 1, text_upper_right, key_size / 2 - 1, 0, 0, 0, 1)
    end
end

function node.render()
    if data.keys == nil then
        gl.clear(1, 0, 0, 1)
        local text_width = dejavu_sans:width("?", 200)
        dejavu_sans:write((WIDTH - text_width) / 2, (HEIGHT - 200) / 2, "?", 200, 1, 1, 1, 1)
        return
    end
    local num_keys = table.getn(data.keys)
    for key_idx = 1, num_keys do
        local key_info = data.keys[key_idx]
        draw_key(data.meta, {descender=data.descender, key_width=data.width}, key_info.x, key_info.y) --TODO labels
    end
end
