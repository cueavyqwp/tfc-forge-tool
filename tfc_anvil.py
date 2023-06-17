from tkinter import ttk
import tkinter as tk
import json
import pip

font = ( "Consolas" , 14 , "bold" )

while 1 :
    try :
        import langful
        break
    except :
        pip.main( [ "install" , "langful" ] )

with open( "data.json" , encoding = "utf-8" ) as file :
    data = json.load( file )
lang = langful.lang( default_lang = "zh_cn" , file_type = "lang" )
root = tk.Tk()
root.title( lang.get("title") )
root.geometry( "400x400" )
root.resizable( 0 , 0 )

def get_name( i : dict ) :
    return lang.str_replace( i["name"] )

forge = {}
item = {}
for i in data["forge"] :
    forge[ i["name"] ] = [ get_name(i) , i["value"] ]
for i in data["item"] :
    value = 0
    for I in [ i["value"] ] + [ -forge[I][1] for I in i["end"] ] :
        value += I
    item[ get_name(i) ] = value
forge_nums = { i[1] : i[0] for i in forge.values() }

combobox = ttk.Combobox( root , justify = tk.CENTER )
combobox["value"] = tuple( item.keys() )
combobox["state"] = "readonly"
combobox.current(0)
combobox.pack( fill = tk.X )

frame_start = ttk.Frame()
tk.Label( frame_start , text = lang.get("start") ).pack( side = tk.LEFT )
start_text = ttk.Entry( frame_start , font = font )
start_text.pack( fill = tk.X )
def start_text_init() :
    start_text.delete( "0" , tk.END )
    start_text.insert( "0" , 0 )
start_text_init()
frame_start.pack( fill = tk.X )

button = ttk.Button( root , text = lang.get("output") )
button.pack( side = tk.BOTTOM )

text = tk.Text( root , font = font )
text.pack( anchor = tk.CENTER , fill = tk.BOTH )
def output_text( text = "" ) :
    text

def output() :
    num = item[ combobox.get() ]
    while 1 :
        try :
            start = start_text.get()
            num += int(start)
            break
        except :
            start_text_init()
    print(num)
button.config( command = output )

root.mainloop()
