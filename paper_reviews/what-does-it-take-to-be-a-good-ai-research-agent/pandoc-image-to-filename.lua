-- Pandoc Lua filter: show only image basenames and make long names wrap.
-- Also strips the image folder path when it appears as plain text.
local path = require 'pandoc.path'
local util = require 'pandoc.utils'

local function escape_latex(text)
  return text:gsub('[\\%%{}%$#&_~^]', function(ch)
    return '\\' .. ch
  end)
end

-- Ensure LaTeX has seqsplit for better line breaking of long filenames.
function Pandoc(doc)
  if FORMAT:match('latex') then
    local header = pandoc.RawBlock('latex', '\\usepackage{seqsplit}')
    doc.meta['header-includes'] = doc.meta['header-includes'] or {}
    table.insert(doc.meta['header-includes'], header)
  end
  return doc
end

-- Replace image nodes with their basename, formatted to allow breaking.
function Image(img)
  local name = path.filename(img.src)
  if FORMAT:match('latex') then
    name = escape_latex(name)
    return { pandoc.RawInline('latex', '\\texttt{\\seqsplit{' .. name .. '}}') }
  end
  return { pandoc.Code(name) }
end

-- Strip the image directory from plain text occurrences.
function Str(el)
  local text = el.text
  local cleaned = text:gsub('%.?/?.-2511%.15593v1%-images/', '')
  if cleaned ~= text then
    return pandoc.Str(cleaned)
  end
end
