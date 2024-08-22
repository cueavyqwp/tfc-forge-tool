import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import traceback
import itertools
import tkinter
import typing
import locale
import json
import os

os.chdir( os.path.dirname( __file__ ) )

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

class lang :

    def __init__( self , path : str = "lang" , default : str = "en_us" ) -> None :
        self.languages : dict[ str , dict[ str , str ] ] = {}
        # get language code
        try :
            code = __import__( "_locale" )._getdefaultlocale()[ 0 ]
        except ( ModuleNotFoundError , AttributeError ) :
            code = locale.getlocale()[ 0 ]
        if os.name == "nt" and code and code[ : 2 ] == "0x" :
            code = locale.windows_locale[ int( code , 0 ) ]
        self.locale = str( code ).replace( "-" , "_" ).lower()
        # init
        for file in os.listdir( path ) :
            file = os.path.join( path , file )
            if not os.path.isfile( file ) or os.path.splitext( file )[ -1 ] != ".lang" : continue
            with open( file , "r" , encoding = "utf-8" ) as fp : data = fp.read()
            language = {}
            for line in data.splitlines() :
                line = line.partition( "#" )[ 0 ]
                key , sep , value = line.partition( "=" )
                if sep : language[ key.strip() ] = value.strip()
            self.languages[ os.path.splitext( os.path.split( file )[ -1 ] )[ 0 ] ] = language
        if self.locale not in self.languages : self.locale = default

    def __getitem__( self , key : str ) -> str :
        return str( self.languages[ self.locale ].get( key ) )

class main :

    def __init__( self , forge : dict[ str , int ] , font : list = [ "Microsoft YaHei" , 16 , "bold" ] , color : bool = True , split : bool = True ) -> None :
        self.config = { "color" : color , "split" : split }
        self.root = tkinter.Tk()
        self.lang = lang()
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

    def join( self , list : list[ list ] ) -> list[ str ] :
        ret = [ list[ 0 ] ]
        for i in list[ 1 : ] :
            if ret[ -1 ][ 0 ] == i[ 0 ] :
                ret[ -1 ][ -1 ] += i[ -1 ]
            else :
                ret.append( i )
        return [ f"{ self.lang[ name ] } * { num }" for name , num in ret ]

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
            [ self.combobox[ i ].current( list( self.forge_name.values() ).index( data[ "end" ][ i ] ) ) for i in range( len( self.combobox ) ) ]
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

    def get_steps( self , data : list ) -> int :
        ret = 0
        for item in data : ret += item[ 1 ]
        return ret

    def possible_way( self , end : int , *args : str | list[ str ] ) -> tuple[ tuple[ str , ... ] , ... ] :
        values = []
        ret = []
        for arg in args :
            if isinstance( arg , str ) : values.append( [ arg ] )
            else : values.append( arg )
        for comb in itertools.product( *values ) :
            num = sum( self.forge[ i ] for i in comb ) + end
            if num < 0 or num > 150 : continue
            ret.append( comb )
        return tuple( ret )

    def calc( self , start : int , end : int ) -> None | list[ list[ str | int ] ] :
        ret = []
        for i in sorted( self.forge.values() , key = lambda x : x + sum( abs( i ) for i in self.forge.values() ) if x < 0 else - x ) :
            while [ ( start + i <= end ) and ( start + i <= 150 ) , ( start + i >= end ) and ( start + i >= 0 ) ][ i < 0 ] :
                start += i
                ret.append( [ self.forge_nums[ i ] , 1 ] )
        while start != end :
            ret.append( [ "forge.hit_light" , 1 ] )
            if start < end :
                start += 1
                ret.append( [ "forge.punch" , 2 ] )
            else :
                start -= 1
                ret.append( [ "forge.punch" , 1 ] )
        if end <= 0 or end >= 150 :
            return None
        return ret

    def calc_get( self ) -> None | tuple[ list , list ]:
        start , end = self.pos
        args : list[ str | list[ str ] ] = []
        for name in ( i.get() for i in self.combobox ) :
            if name == self.lang[ "forge.any" ] : args.append( list( self.forge.keys() ) )
            else : args.append( self.forge_name[ name ] )
        ways = self.possible_way( end , *args )
        if not ways : return None
        ret = []
        for way in ways :
            forge_way = self.calc( start , end - sum( self.forge[ name ] for name in way ) )
            if forge_way is None : continue
            forge_end = [ [ value , 1 ] for value in way ]
            forge_end.reverse()
            ret.append( ( forge_way , forge_end ) )
        ret.sort( key = lambda item : self.get_steps( item[ 0 ] ) )
        if not ret : return None
        return ret[ 0 ]

    def output( self , *args ) -> None :
        self.clear()
        line = 1
        ret = self.calc_get()
        if ret is None :
            self.print( self.lang[ "error" ] , cls = True )
            if self.config[ "color" ] : self.info.tag_add( "error" , f"1.0" , f"2.0" )
            return None
        ret = [ self.join( list( value ) ) for value in ret ]
        for text in ( *ret[ 0 ] , None , *ret[ 1 ] ) :
            if text is None :
                if self.config[ "split" ] :
                    self.print( "\n" )
                    line += 1
                continue
            self.print( f"{ text }\n" )
            if self.config[ "color" ] :
                name , num = text.split( " * " )
                self.info.tag_add( "forge" , f"{ line }.0" , f"{ line }.{ len( name ) }" )
                self.info.tag_add( "num" , f"{ line }.{ len( name ) + 3 }" , f"{ line }.{ len( name ) + 3 + len( num ) }" )
            line += 1

    def init( self ) -> None :
        # values
        self.forge_name = { self.lang[ key ] : key for key in [ *self.forge.keys() , "forge.any" ] }
        print(self.forge_name)
        self.forge_nums = { v : k for k , v in self.forge.items() }
        # create save dir
        self.save_path = os.path.join( "." , "save" )
        None if os.path.exists( self.save_path ) else os.mkdir( self.save_path )
        # frames
        frame_top = tkinter.Frame( self.root )
        frame_option = tkinter.Frame( frame_top )
        frame_combobox = tkinter.Frame( frame_option )
        # pos entry
        self.entry : list[ tkinter.ttk.Entry ] = []
        for name in [ "pos.start" , "pos.end" ] :
            frame = tkinter.Frame( frame_option )
            tkinter.Label( frame , text = self.lang[ name ] ).pack( side = "left" , fill = "x" )
            pos = tkinter.ttk.Entry( frame , font = self.font )
            pos.pack( side = "right" , expand = True , fill = "x" )
            self.entry.append( pos )
            frame.pack( side = "top" , fill = "x" , padx = 1 , pady = 1 )
        self.pos
        # combobox
        tkinter.Label( frame_combobox , text = self.lang[ "end" ] ).pack( side = "left" )
        self.combobox : list[ tkinter.ttk.Combobox ] = []
        for _ in range( 3 ) :
            combobox = tkinter.ttk.Combobox( frame_combobox , values = list( self.forge_name.keys() ) , state = "readonly" )
            combobox.current( 0 )
            combobox.pack( side = "top" , expand = True , fill = "x" , padx = 1 , pady = 1 , ipady = 5 )
            self.combobox.append( combobox )
        # output button
        tkinter.ttk.Button( frame_top , text = self.lang[ "output" ] , command = self.output ).pack( side = "right" , expand = True , fill = "both" , padx = 1 , pady = 1 )
        # pack frames
        frame_top.pack( side = "top" , fill = "x" )
        frame_option.pack( side = "left" )
        frame_combobox.pack( side = "top" , expand = True , fill = "x" )
        # load & save button
        [ tkinter.ttk.Button( frame_option , text = self.lang[ text ] , command = func ).pack( side = "top" , expand = True , fill = "both" , padx = 1 , pady = 1 ) for text , func in [ [ "save" , self.save ] , [ "load" , self.load ] ] ]
        # info text
        self.info = tkinter.scrolledtext.ScrolledText( self.root , relief = "ridge" , font = self.font )
        self.info.pack( side = "bottom" , expand = True , fill = "both" )
        self.clear()
        # key bindings
        [ self.root.bind( f"<{ key }>" , func ) for key , func in [ [ "Return" , self.output ] , [ "Control-l" , self.load ] , [ "Control-s" , self.save ] , [ "Delete" , self.clear ] ] ]
        # colorful
        if self.config[ "color" ] : [ self.info.tag_config( name , foreground = color ) for name , color in [ [ "forge" , "purple" ] , [ "num" , "yellowgreen" ] , [ "error" , "red" ] ] ]

if __name__ == "__main__" :
    root = main( forge )
    root.run()
