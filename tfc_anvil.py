import tkinter as tk
import json
import pip

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
for i in data["forge"] :
    forge[ i["name"] ] = [ get_name(i) , i["value"] ]
print(forge)
item = {}
for i in data["item"] :
    value = 0
    for I in [ i["value"] ] + [ -forge[I][1] for I in i["end"] ] :
        value += I
    item[ i["name"] ] = [ get_name(i) , value ]

print(item)

root.mainloop()
