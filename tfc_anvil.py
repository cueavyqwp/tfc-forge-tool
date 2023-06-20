from tkinter.filedialog import askopenfilename , asksaveasfilename
from tkinter.ttk import Combobox , Button , Entry
from tkinter.scrolledtext import ScrolledText
from tkinter.messagebox import showerror
from tkinter import Frame , Label , Tk
import json
import pip
import os

is_debug = True
font = ( "Consolas" , 18 , "bold" )

while 1 :
    try :
        import langful
        break
    except :
        pip.main( [ "install" , "langful" ] )
save_path = os.path.join( os.path.split(__file__)[0] , "save" )
if not os.path.exists( save_path ) :
    os.mkdir( save_path )

lang = langful.lang( lang_dir = os.path.join( os.path.split(__file__)[0] , "lang" ) , default_lang = "en_us" , file_type = "lang" )
root = Tk()
root.title( lang.get("title") )
root.geometry( f"400x700" )
root.attributes( "-topmost" , 1 )
root.attributes( "-transparent" )
root.update()

forge = {
    "forge.hit_light" : -3 ,
    "forge.hit_medium" : -6 ,
    "forge.hit_hard" : -9 ,
    "forge.draw" : -15 ,
    "forge.punch" : 2 ,
    "forge.bend" : 7 ,
    "forge.upset" : 13 ,
    "forge.shrink" : 16
}

def forge_name() : return { lang.get(i) : i for i in forge }
def forge_nums() : return { v : k for k , v in forge.items() }

info_frame = Frame()

output_button = Button( info_frame , text = lang.get( "output" ) )
output_button.pack( side = "right" , anchor="e" , fill = "both" )

save_button = Button( root , text = lang.get("save") )
save_button.pack( side = "bottom" , fill =  "x" )

load_button = Button( root , text = lang.get("load") )
load_button.pack( side = "bottom" , fill =  "x" )

start_frame = Frame(info_frame)
Label( start_frame , text = lang.get("start") ).pack( side = "left" )
start_text = Entry( start_frame , font = font )
start_text.pack( fill = "x" )
def start_text_init( num = 0 ) :
    start_text.delete( "0" , "end" )
    start_text.insert( "0" , num )
start_text_init()
start_frame.pack( fill = "x" )

end_frame = Frame(info_frame)
Label( end_frame , text = lang.get("end_p") ).pack( side = "left" )
end_text = Entry( end_frame , font = font )
end_text.pack( fill = "x" )
def end_text_init( num = 0 ) :
    end_text.delete( "0" , "end" )
    end_text.insert( "0" , num )
end_text_init()
end_frame.pack( fill = "x" )

end_combobox = []
Label( info_frame , text = lang.get( "end" ) ).pack( side = "left" )
for i in range(3) :
    end_combobox.append( Combobox( info_frame ) )
    end_combobox[-1]["value"] = tuple( forge_name().keys() )
    end_combobox[-1]["state"] = "readonly"
    end_combobox[-1].current(0)
    end_combobox[-1].pack( fill = "x" )

info_frame.pack( fill = "x" )

text = ScrolledText( root , relief = "ridge" , font = font , height = root.winfo_height() )
text.pack( anchor = "center" , fill = "both" )
def output_text( info = "" , end = "\n" , cls = False ) :
    text.config( state = "normal" )
    if cls :
        text.delete( "0.0" , "end" )
        end = ""
    text.insert( "end" , str( info ) + end )
    text.config( state = "disabled" )
output_text("")

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

def file_load() :
    path = askopenfilename( initialdir = ".\\save" )
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
            num = list( forge.keys() ).index( data["end"][i] )
            end_combobox[i].current( num )
        output()
    except Exception as e :
        showerror( lang.get("error") , e )

def file_save() :
    path = asksaveasfilename( initialdir = ".\\save" , initialfile = "data" , filetypes = [ [ "JSON" , ".json" ] ] )
    if not path :
        return
    path += ".json"
    debug(path)
    data = {}
    data["pos"] = [ start_text.get() , end_text.get() ]
    data["end"] = [ forge_name()[ i.get() ] for i in end_combobox ]
    debug(data)
    try :
        with open( path , "w" , encoding = "utf-8" ) as file :
            file.write( json.dumps( data , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False ) )
    except Exception as e :
        showerror( lang.get("error") , e )

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
        num -= forge[ forge_name()[ i.get() ] ]
    l = list( forge.values() )
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
            ret.append( [ forge_nums()[i] , 1 ] )
    for i in sub :
        while ( I + i >= num ) and ( I + i >= 0 ) :
            I += i
            ret.append( [ forge_nums()[i] , 1 ] )
    while I != num :
        ret.append( [ "forge.hit_light" , 1 ] )
        if I < num :
            I += 1
            ret.append( [ "forge.punch" , 2 ] )
        else :
            I -= 1
            ret.append( [ "forge.punch" , 1 ] )
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
load_button.config( command = file_load )
save_button.config( command = file_save )
root.mainloop()
