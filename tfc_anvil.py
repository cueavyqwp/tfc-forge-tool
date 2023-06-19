from tkinter import scrolledtext , messagebox , filedialog , ttk
import tkinter as tk
import json
import pip

font = ( "Consolas" , 18 , "bold" )

while 1 :
    try :
        import langful
        break
    except :
        pip.main( [ "install" , "langful" ] )

lang = langful.lang( default_lang = "en_us" , file_type = "lang" )
# debug
# lang.use_locale="en_us"
# lang.use_locale="zh_cn"
win_size = 400 , 700
x , y = 0 , 0
is_debug = True
root = tk.Tk()
root.title( lang.get("title") )
root.geometry( f"{win_size[0]}x{win_size[1]}+200+200" )
root.attributes( "-topmost" , 1 )
root.attributes( "-transparent" )
root.update()

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

info_frame = tk.Frame()

output_button = ttk.Button( info_frame , text = lang.get( "output" ) )
output_button.pack( side = tk.RIGHT , anchor=tk.E , fill = tk.BOTH )

save_button = ttk.Button( root , text = lang.get("save") )
save_button.pack( side = tk.BOTTOM , fill =  tk.X )

load_button = ttk.Button( root , text = lang.get("load") )
load_button.pack( side = tk.BOTTOM , fill =  tk.X )

start_frame = tk.Frame(info_frame)
tk.Label( start_frame , text = lang.get("start") ).pack( side = tk.LEFT )
start_text = ttk.Entry( start_frame , font = font )
start_text.pack( fill = tk.X )
def start_text_init( num = 0 ) :
    start_text.delete( "0" , tk.END )
    start_text.insert( "0" , num )
start_text_init()
start_frame.pack( fill = tk.X )

end_frame = tk.Frame(info_frame)
tk.Label( end_frame , text = lang.get("end_p") ).pack( side = tk.LEFT )
end_text = ttk.Entry( end_frame , font = font )
end_text.pack( fill = tk.X )
def end_text_init( num = 0 ) :
    end_text.delete( "0" , tk.END )
    end_text.insert( "0" , num )
end_text_init()
end_frame.pack( fill = tk.X )

end_combobox = []
tk.Label( info_frame , text = lang.get( "end" ) ).pack( side = "left" )
for i in [ [tk.N,tk.LEFT] , [tk.NW,tk.RIGHT] , [tk.NE,tk.LEFT] ] :
    end_combobox.append( ttk.Combobox( info_frame ) )
    end_combobox[-1]["value"] = tuple( forge_name.keys() )
    end_combobox[-1]["state"] = "readonly"
    end_combobox[-1].current(0)
    end_combobox[-1].pack( fill = tk.X )

info_frame.pack( fill = tk.X )

text = scrolledtext.ScrolledText( root , relief = tk.RIDGE , font = font , height = root.winfo_height() )
text.pack( anchor = tk.CENTER , fill = tk.BOTH )
def output_text( info = "" , end = "\n" , cls = False ) :
    text.config( state = tk.NORMAL )
    if cls :
        text.delete( "0.0" , tk.END )
        end = ""
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

def debug( text ) :
    if is_debug :
        print( text )

def join( list ) :
    ret = [ list[0] ]
    list = list[1:]
    for i in list :
        if ret[-1][0] == i[0] :
            ret[-1][-1] += i[-1]
        else :
            ret.append(i)
    return ret

def load() :
    path = filedialog.askopenfilename( initialdir = "./" )
    if not path :
        return
    debug(path)
    try :
        with open( path , encoding = "utf-8" ) as file :
            data = json.load( file )
        start , end = data["pos"]
        start_text_init( start )
        end_text_init( end )
        for i in range(3) :
            num = list( forge_nums.keys() ).index( data["end"][i] )
            end_combobox[i].current( num )
        output()
    except Exception as e :
        messagebox.showerror( lang.get("error") , e )

def save() :
    path = filedialog.asksaveasfilename( initialdir = "./" , initialfile = "data" , filetypes = [ [ "JSON" , ".json" ] ] )
    if not path :
        return
    path += ".json"
    debug(path)
    data = {}
    data["pos"] = [ start_text.get() , end_text.get() ]
    data["end"] = [ forge_name[ i.get() ] for i in end_combobox ]
    debug(data)
    try :
        with open( path , "w" , encoding = "utf-8" ) as file :
            file.write( json.dumps( data , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )
    except Exception as e :
        messagebox.showerror( lang.get("error") , e )

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
    num = end
    for i in end_combobox :
        num -= forge_nums[ forge_name[ i.get() ] ]
    l = list( forge_nums.values() )
    l.sort()
    I = start
    ret = []
    add = []
    sub = []
    for i in l :
        if i < 0 :
            sub.append(i)
        else :
            add.append(i)
    add.reverse()
    for i in add :
        while ( I + i <= num ) and ( I + i <= 150 ) :
            I += i
            ret.append( [ forge_nums_name[i] , 1 ] )
    for i in sub :
        while ( I + i >= num ) and ( I + i >= 0 ) :
            I += i
            ret.append( [ forge_nums_name[i] , 1 ] )
    while I < num :
        I += 1
        ret.append( [ "forge.punch" , 2 ] )
        ret.append( [ "forge.hit_light" , 1 ] )
    while I > num :
        I -= 1
        ret.append( [ "forge.punch" , 1 ] )
        ret.append( [ "forge.hit_light" , 1 ] )
    debug( f"{I}|{num}|{end}" )
    debug( [ i[0] for i in ret ] )
    if num <= 0 or num >= 150 :
        output_text( "error" , cls = True )
        return
    end_forge = []
    for i in end_combobox :
        end_forge.append( [ i.get() , 1 ] )
    end_forge.reverse()
    ret = [ [ lang.get(i[0]) , i[1] ] for i in ret ]
    for i in join( ret ) :
        output_text( f"{i[0]} * {i[1]}" )
    output_text()
    for i in join( end_forge ) :
        output_text( f"{i[0]} * {i[1]}" )

output_button.config( command = output )
load_button.config( command = load )
save_button.config( command = save )
root.bind( "<B3-Motion>" , move )
root.bind( "<Button-3>" , get_point )
root.mainloop()
