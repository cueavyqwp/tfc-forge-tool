import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import traceback
import tkinter
import typing
import json
import os

os.chdir( os.path.dirname( __file__ ) )

for _ in range( 3 ) :
    try :
        import langful
        break
    except ModuleNotFoundError :
        import subprocess
        import sys
        subprocess.check_call( [ sys.executable , "-m" , "pip" , "install" , "langful" ] )
else :
    raise ImportError( "can't import or install module" )

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

class main :

    def __init__( self , forge : dict[ str , int ] , font : list = [ "Microsoft YaHei" , 16 , "bold" ] , color : bool = True , split : bool = True ) -> None :
        self.config = { "color" : color , "split" : [ [] , [ "" ] ][ split ] }
        self.lang = langful.lang()
        self.root = tkinter.Tk()
        if os.name == "nt" : self.root.attributes( "-topmost" , True )
        self.root.protocol( "WM_DELETE_WINDOW" , self.exit )
        self.root.title( self.lang[ "title" ] )
        self.root.geometry( f"400x700" )
        self.forge = forge
        self.font = font

    def exit( self , code = None ) -> None :
        if code is None : code = 0
        self.root.destroy()
        exit( code )

    def run( self ) -> None :
        self.init()
        try :
            self.root.mainloop()
        except KeyboardInterrupt :
            self.exit( 0 )
        traceback.print_exc()
        self.exit( 1 )

    @property
    def pos( self ) -> list :
        ret = []
        for entry in self.entry :
            if ( text := entry.get() ).isalnum() and ( i := int( text ) ) > 0 and i < 150 :
                ret.append( i )
            else :
                ret.append( 0 )
                entry.delete( 0 , "end" )
                entry.insert( 0 , "0" )
        return ret

    def join( self , list : list ) -> list[ str ] :
        ret = [ list[ 0 ] ]
        for i in list[ 1 : ] :
            if ret[ -1 ][ 0 ] == i[ 0 ] :
                ret[ -1 ][ -1 ] += i[ -1 ]
            else :
                ret.append( i )
        return [ f"{ name } * { num }" for name , num in ret ]

    def trydo( self , func : typing.Callable ) -> None :
        try : func( self )
        except : tkinter.messagebox.showerror( self.lang[ "error" ] , traceback.format_exc() )

    def load( self , *args ) -> None :
        path = tkinter.filedialog.askopenfilename( initialdir = self.save_path )
        if not path : return
        def func( self : main ) -> None :
            with open( path , encoding = "utf-8" ) as file : data = json.load( file )
            entry = self.entry[ -1 ]
            entry.delete( 0 , "end" )
            entry.insert( 0 , str( data[ "pos" ] ) )
            [ self.combobox[ i ].current( list( self.forge.keys() ).index( data[ "end" ][ i ] ) ) for i in range( len( self.combobox ) ) ]
            self.output()
        self.trydo( func )

    def save( self , *args ) -> None :
        path = tkinter.filedialog.asksaveasfilename( initialdir = self.save_path , initialfile = "" , filetypes = [ ( "JSON" , ".json" ) ] )
        if not path : return
        if ( len( path ) < 5 ) or ( ".json" not in path ) : path += ".json"
        data = { "pos" : self.pos[ -1 ] , "end" : [ self.forge_name[ combobox.get() ] for combobox in self.combobox ] }
        def func( self : main ) -> None :
            with open( path , "w" , encoding = "utf-8" ) as file : json.dump( data , file , indent = 4 , separators = ( " ," , ": " ) , ensure_ascii = False )
        self.trydo( func )

    def info_edit( self , func : typing.Callable ) -> None :
        self.info.config( state = "normal" )
        func( self )
        self.info.config( state = "disabled" )

    def cls( self , *args ) -> None :
        self.info.delete( 0.0 , "end" )

    def clear( self , *args ) -> None :
        self.info_edit( self.cls )

    def print( self , text : str = "" , cls : bool = False ) -> None :
        def func( self : main ) -> None :
            if cls : self.cls()
            self.info.insert( "end" , str( text ) )
        self.info_edit( func )

    def color( self , texts : list[ str ] ) -> None :
        for text , i in zip( texts , [ f"{ i + 1 }." for i in range( len( texts ) ) ] ) :
            if not text : continue
            forge , num = [ len( s ) for s in text.split( " * " ) ]
            [ self.info.tag_add( *value ) for value in [ [ "forge" , i + "0" , i + str( forge ) ] , [ "num" , i + str( len( text ) - num ) , i + str( len( text ) ) ] ] ]
        [ self.info.tag_config( name , foreground = color ) for name , color in [ [ "forge" , "purple" ] , [ "num" , "yellowgreen" ] ] ]

    def output( self , *args ) -> None :
        self.clear()
        num , end = self.pos
        l = list( self.forge.values() )
        ret = []
        end -= sum( self.forge[ self.forge_name[ i.get() ] ] for i in self.combobox )
        for i in sorted( l , key = lambda x : x + sum( abs( i ) for i in l ) if x < 0 else - x ) :
            while [ ( num + i <= end ) and ( num + i <= 150 ) , ( num + i >= end ) and ( num + i >= 0 ) ][ i < 0 ] :
                num += i
                ret.append( [ self.forge_nums[ i ] , 1 ] )
        while num != end :
            ret.append( [ "forge.hit_light" , 1 ] )
            if num < end :
                num += 1
                ret.append( [ "forge.punch" , 2 ] )
            else :
                num -= 1
                ret.append( [ "forge.punch" , 1 ] )
        if end <= 0 or end >= 150 :
            self.print( self.lang[ "error" ] , cls = True )
        else :
            end_forge = self.join( list( reversed( [ [ i.get() , 1 ] for i in self.combobox ] ) ) )
            ret = self.join( [ [ self.lang[ i[ 0 ] ] , i[ 1 ] ] for i in ret ] ) if ret else []
            self.print( s := "\n".join( [ i for i in [ [] , ret + self.config[ "split" ] ][ bool( ret ) ] + end_forge ] ) )
            if self.config[ "color" ] : self.color( str( s ).splitlines() )

    def init( self ) -> None :
        # values
        self.forge_name = { self.lang[ i ] : i for i in forge }
        self.forge_nums = { v : k for k , v in forge.items() }
        # create save dir
        self.save_path = os.path.join( "." , "save" )
        None if os.path.exists( self.save_path ) else os.mkdir( self.save_path )
        # frames
        top_frame = tkinter.Frame( self.root )
        option_frame = tkinter.Frame( top_frame )
        combobox_frame = tkinter.Frame( option_frame )
        # pos entry
        self.entry : list[ tkinter.ttk.Entry ] = []
        for name in [ "pos.start" , "pos.end" ] :
            frame = tkinter.Frame( option_frame )
            tkinter.Label( frame , text = self.lang[ name ] ).pack( side = "left" , fill = "x" )
            pos = tkinter.ttk.Entry( frame , font = self.font )
            pos.pack( side = "right" , expand = True , fill = "x" )
            self.entry.append( pos )
            frame.pack( side = "top" , fill = "x" , padx = 1 , pady = 1 )
        self.pos
        # combobox
        tkinter.Label( combobox_frame , text = self.lang[ "end" ] ).pack( side = "left" )
        self.combobox : list[ tkinter.ttk.Combobox ] = []
        for _ in range( 3 ) :
            combobox = tkinter.ttk.Combobox( combobox_frame , values = list( self.forge_name.keys() ) , state = "readonly" )
            combobox.current( 0 )
            combobox.pack( side = "top" , expand = True , fill = "x" , padx = 1 , pady = 1 , ipady = 5 )
            self.combobox.append( combobox )
        # output button
        tkinter.ttk.Button( top_frame , text = self.lang[ "output" ] , command = self.output ).pack( side = "right" , expand = True , fill = "both" , padx = 1 , pady = 1 )
        # pack frames
        top_frame.pack( side = "top" , fill = "x" )
        option_frame.pack( side = "left" )
        combobox_frame.pack( side = "top" , expand = True , fill = "x" )
        # load & save button
        [ tkinter.ttk.Button( option_frame , text = self.lang[ text ] , command = func ).pack( side = "top" , expand = True , fill = "both" , padx = 1 , pady = 1 ) for text , func in [ [ "save" , self.save ] , [ "load" , self.load ] ] ]
        # info text
        self.info = tkinter.scrolledtext.ScrolledText( self.root , relief = "ridge" , font = self.font )
        self.info.pack( side = "bottom" , expand = True , fill = "both" )
        self.clear()
        # key bindings
        [ self.root.bind( f"<{ key }>" , func ) for key , func in [ [ "Return" , self.output ] , [ "Control-l" , self.load ] , [ "Control-s" , self.save ] , [ "Delete" , self.clear ] ] ]

if __name__ == "__main__" :
    root = main( forge )
    root.run()
