from tkinter import scrolledtext , ttk
import tkinter as tk
import pip

font = ( "Consolas" , 18 , "bold" )

while 1 :
    try :
        import langful
        break
    except :
        pip.main( [ "install" , "langful" ] )

lang = langful.lang( default_lang = "en_us" , file_type = "lang" )
# lang.use_locale="en_us"
win_size = 400 , 700
x , y = 0 , 0
root = tk.Tk()
root.title( lang.get("title") )
root.geometry( f"{win_size[0]}x{win_size[1]}+200+200" )
root.resizable( 0 , 0 )
root.overrideredirect(1)
root.attributes( "-topmost" , 1 )
root.attributes( "-transparent" )

forge = [{
    "name" : "forge.hit_light" ,
    "value" : -3
} , {
    "name" : "forge.hit_medium" ,
    "value" : -6
} , {
    "name" : "forge.hit_hard" ,
    "value" : -9
} , {
    "name" : "forge.draw" ,
    "value" : -15
} , {
    "name" : "forge.bend" ,
    "value" : 7
} , {
    "name" : "forge.punch" ,
    "value" : 2
} , {
    "name" : "forge.shrink" ,
    "value" : 16
} , {
    "name" : "forge.upset" ,
    "value" : 13
}]

forge_nums = { i["name"] : i["value"] for i in forge }
forge_name = { lang.get(i) : i for i in forge_nums }
forge_nums_name = { v : k for k , v in forge_nums.items() }

frame_start = tk.Frame()
tk.Label( frame_start , text = lang.get("start") ).pack( side = tk.LEFT )
start_text = ttk.Entry( frame_start , font = font )
start_text.pack( fill = tk.X )
def start_text_init() :
    start_text.delete( "0" , tk.END )
    start_text.insert( "0" , 0 )
start_text_init()
frame_start.pack( fill = tk.X )

frame_end = tk.Frame()
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
    end_combobox[-1]["value"] = tuple( forge_name.keys() )
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
    text.insert( tk.END , str( info ) + end )
    text.config( state = tk.DISABLED )
output_text("")

def move( event ) :
    set_x = event.x - x + root.winfo_x()
    set_y = event.y - y + root.winfo_y()
    root.geometry(f"{win_size[0]}x{win_size[1]}+{set_x}+{set_y}")

def get_point( event ) :
    global x , y
    x = event.x
    y = event.y

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
    num = end-start
    for i in end_combobox :
        num -= forge_nums[ forge_name[ i.get() ] ]
    if num <= 0 or num >= 150 :
        output_text( "error" , cls = True )
        return
    l = list( forge_nums.values() )
    l.sort()
    I = 0
    ret = []
    add = []
    sub = []
    for i in l :
        if i < 0 :
            sub.append(i)
        else :
            add.append(i)
    while I < num :
        for i in add :
            if I < num :
                I += i
                ret.append( [ forge_nums_name[i] , 1 ] )
    if I > num :
        for i in sub :
            if ( num - I ) % i == 0 :
                while I == num :
                    I += I
                    ret.append( [ forge_nums_name[i] , 1 ] )
    for i in [ 4 , 1 ] :
        if ( num - I ) % i == 0 :
            while I > num :
                I -= i
                match i :
                    case 1 :
                        ret.append( [ "forge.punch" , 1 ] )
                        ret.append( [ "forge.hit_light" , 1 ] )
                    case 4 :
                        ret.append( [ "forge.upset" , 1 ] )
                        ret.append( [ "forge.hit_hard" , 1 ] )
    # debug
    print(I)
    print(num)
    print(ret)
    for i in ret :
        output_text( f"{lang.get(i[0])} * {i[1]}" )
    output_text()
    for i in range( len( end_combobox ) - 1 , -1 , -1 ) :
        output_text( f"{ end_combobox[i].get() } * 1" )
def close( event ) :
    root.destroy()
    quit()
button.config( command = output )
root.bind( "<B3-Motion>" , move )
root.bind( "<Button-3>" , get_point )
root.bind( "<Escape>" , close )
root.mainloop()
