from tkinter import scrolledtext , ttk
import tkinter as tk
import pip

font = ( "Consolas" , 20 , "bold" )

while 1 :
    try :
        import langful
        break
    except :
        pip.main( [ "install" , "langful" ] )

lang = langful.lang( default_lang = "en_us" , file_type = "lang" )
# lang.use_locale="en_us"
root = tk.Tk()
root.title( lang.get("title") )
root.geometry( "400x400" )
root.resizable( 0 , 0 )

def get_name( i : dict ) :
    return lang.str_replace( i["name"] )

forge = [{
    "name" : "%forge.hit_light%" ,
    "value" : -3
} , {
    "name" : "%forge.hit_medium%" ,
    "value" : -6
} , {
    "name" : "%forge.hit_hard%" ,
    "value" : -9
} , {
    "name" : "%forge.draw%" ,
    "value" : -15
} , {
    "name" : "%forge.bend%" ,
    "value" : 7
} , {
    "name" : "%forge.punch%" ,
    "value" : 2
} , {
    "name" : "%forge.shrink%" ,
    "value" : 16
} , {
    "name" : "%forge.upset%" ,
    "value" : 13
}]

forge_nums = { get_name(i) : i["value"] for i in forge }

frame_start = ttk.Frame()
tk.Label( frame_start , text = lang.get("start") ).pack( side = tk.LEFT )
start_text = ttk.Entry( frame_start , font = font )
start_text.pack( fill = tk.X )
def start_text_init() :
    start_text.delete( "0" , tk.END )
    start_text.insert( "0" , 0 )
start_text_init()
frame_start.pack( fill = tk.X )

frame_end = ttk.Frame()
tk.Label( frame_end , text = lang.get("end_p") ).pack( side = tk.LEFT )
end_text = ttk.Entry( frame_end , font = font )
end_text.pack( fill = tk.X )
def end_text_init() :
    end_text.delete( "0" , tk.END )
    end_text.insert( "0" , 0 )
end_text_init()
frame_end.pack( fill = tk.X )

frame_end_combobox = ttk.Frame()
end_combobox = []
tk.Label( frame_end_combobox , text = lang.get( "end" ) ).pack( side = "left" )
for i in [ [tk.N,tk.LEFT] , [tk.NW,tk.RIGHT] , [tk.NE,tk.LEFT] ] :
    end_combobox.append( ttk.Combobox( frame_end_combobox ) )
    end_combobox[-1]["value"] = tuple( forge_nums.keys() )
    end_combobox[-1]["state"] = "readonly"
    end_combobox[-1].current(0)
    end_combobox[-1].pack( fill = tk.X )
frame_end_combobox.pack(fill="x")

button = ttk.Button( root , text = lang.get("output") )
button.pack( side = tk.BOTTOM , fill = "x" )

text = scrolledtext.ScrolledText( root , relief = tk.RIDGE , font = font )
text.pack( anchor = tk.CENTER , fill = tk.BOTH )
def output_text( info = "" , end = "\n" , cls = False ) :
    text.config( state = tk.NORMAL )
    if cls :
        text.delete( "0.0" , tk.END )
    else :
        text.insert( tk.END , str( info ) + end )
    text.config( state = tk.DISABLED )
output_text("")

def output() :
    output_text( cls = True )
    while 1 :
        try :
            start = start_text.get()
            start = int(start)
            break
        except :
            start_text_init()
    while 1 :
        try :
            end = end_text.get()
            end = int(end)
            break
        except :
            end_text_init()
    num = start + end
    print(num)
    l = list( forge_nums.keys() )
    l.sort()
    ret = []
    i = 0
    # while not i == num :
    #     for I in l :
    #         if I >= 0 :
    #             if i + I <= num :
    #                 i += I
    #         else :
    #             if ( i > num ) and ( i >= -I ) :
    #                 i += I
    #                 ret.append(forge_nums[I])
    #     print(i)
    output_text()
    for i in end_combobox :
        output_text( f"{i.get()} * 1" )
button.config( command = output )
root.mainloop()
