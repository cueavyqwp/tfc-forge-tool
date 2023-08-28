import tkinter.scrolledtext
import tkinter.messagebox
import tkinter.filedialog
import tkinter.ttk
import tkinter
import json
import pip
import os

while True :
    try :
        import langful
        break
    except ImportError :
        pip.main( [ "install" , "langful" ] )

os.chdir( os.path.split( __file__ )[ 0 ] )
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

    def __init__( self , forge : dict[ str , int ] , font : list = [ "Consolas" , 18 , "bold" ] , color = True , split = True ) -> None :
        self.lang = langful.lang( os.path.join( os.path.split( __file__ )[ 0 ] , "lang" ) )
        self.config = { "color" : color , "split" : split }
        self.root = tkinter.Tk()
        self.root.title( self.lang[ "title" ] )
        self.root.geometry( f"400x700" )
        self.root.attributes( "-topmost" , True )
        self.root.attributes( "-transparent" )
        self.forge = forge
        self.font = font
        self.root.update()

    def run( self ) -> None :
        self.init()
        self.root.mainloop()

    @property
    def pos( self ) -> None :
        ret = []
        for entry in self.entry :
            num = entry.get()
            try :
                ret.append( int( num ) )
            except :
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

    def load( self ) -> None :
        path = tkinter.filedialog.askopenfilename( initialdir = self.save_path )
        if not path :
            return
        try :
            with open( path , encoding = "utf-8" ) as file :
                data = json.load( file )
            entry = self.entry[ -1 ]
            entry.delete( 0 , "end" )
            entry.insert( 0 , str( data[ "pos" ] ) )
            for i in range( len( self.combobox ) ) :
                num = list( self.forge.keys() ).index( data[ "end" ][ i ] )
                self.combobox[ i ].current( num )
            self.output()
        except Exception as e :
            tkinter.messagebox.showerror( self.lang[ "error" ] , e )

    def save( self ) -> None :
        path = tkinter.filedialog.asksaveasfilename( initialdir = self.save_path , initialfile = "" , filetypes = [ [ "JSON" , ".json" ] ] )
        if not path :
            return
        if ( len( path ) < 5 ) or ( ".json" not in path ) :
            path += ".json"
        data = { "pos" : self.pos[ -1 ] , "end" : [ self.forge_name[ combobox.get() ] for combobox in self.combobox ] }
        try :
            with open( path , "w" , encoding = "utf-8" ) as file :
                json.dump( data , file , indent = 4 , separators = [ " ," , ": " ] , ensure_ascii = False )
        except Exception as e :
            tkinter.messagebox.showerror( self.lang[ "error" ] , e )

    def print( self , text : str = "" , end : str = "\n" , cls : bool = False ) -> None :
        self.info.config( state = "normal" )
        if cls :
            self.info.delete( "0.0" , "end" )
            end = ""
        self.info.insert( "end" , str( text ) + end )
        self.info.config( state = "disabled" )

    def color( self , texts : list[ str ] ) -> None :
        for text , i in zip( texts , [ f"{ i + 1 }." for i in range( len( texts ) ) ] ) :
            if not text : continue
            l = len( text )
            forge , num = [ len( s ) for s in text.split( " * " ) ]
            [ self.info.tag_add( *value ) for value in [ [ "forge" , i + "0" , i + str( forge ) ] , [ "num" , i + str( l - num ) , i + str( l ) ] ] ]
        self.info.tag_config( "forge" , foreground = "purple" )
        self.info.tag_config( "num" , foreground = "yellowgreen" )

    def output( self , *args ) -> None :
        self.print( cls = True )
        num , end = self.pos
        l = list( self.forge.values() )
        ret = []
        for i in self.combobox :
            end -= self.forge[ self.forge_name[ i.get() ] ]
        for i in sorted( l , key = lambda x : x + sum( abs( i ) for i in l ) if x < 0 else - x ) :
            if i < 0 :
                while ( num + i >= end ) and ( num + i >= 0 ) :
                    num += i
                    ret.append( [ self.forge_nums[ i ] , 1 ] )
            else :
                while ( num + i <= end ) and ( num + i <= 150 ) :
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
            end_forge = []
            for i in self.combobox :
                end_forge.append( [ i.get() , 1 ] )
            end_forge.reverse()
            ret = [ [ self.lang[ i[ 0 ] ] , i[ 1 ] ] for i in ret ]
            s = "\n".join( i for i in self.join( ret ) + [ [] , [ "" ] ][ self.config[ "split" ] ] + self.join( end_forge ) )
            self.print( s )
            self.color( s.splitlines() ) if self.config[ "color" ] else ...

    def init( self ) -> None :
        self.forge_name = { self.lang[ i ] : i for i in forge }
        self.forge_nums = { v : k for k , v in forge.items() }
        # create save dir
        self.save_path = os.path.join( os.path.split( __file__ )[ 0 ] , "save" )
        if not os.path.exists( self.save_path ) :
            os.mkdir( self.save_path )
        # frames
        top_frame = tkinter.Frame( self.root )
        option_frame = tkinter.Frame( top_frame )
        combobox_frame = tkinter.Frame( option_frame )
        # output button
        tkinter.ttk.Button( top_frame , text = self.lang[ "output" ] , command = self.output ).pack( side = "right" , expand = True , fill = "both" )
        self.root.bind( "<Return>" , self.output )
        top_frame.pack( side = "top" , fill = "x" )
        # pos entry
        self.entry = []
        for name in [ "pos.start" , "pos.end" ] :
            frame = tkinter.Frame( option_frame )
            tkinter.Label( frame , text = self.lang[ name ] ).pack( side = "left" , fill = "x" )
            pos = tkinter.ttk.Entry( frame , font = self.font )
            pos.pack( side = "right" , expand = True , fill = "x" )
            self.entry.append( pos )
            frame.pack( side = "top" , fill = "x" )
        self.pos
        # combobox
        tkinter.Label( combobox_frame , text = self.lang[ "end" ] ).pack( side = "left" )
        self.combobox = []
        for i in range( 3 ) :
            i = tkinter.ttk.Combobox( combobox_frame , values = list( self.forge_name.keys() ) )
            i.config( state = "readonly" )
            i.current( 0 )
            i.pack( side = "top" , expand = True , fill = "x" , ipady = 4 )
            self.combobox.append( i )
        combobox_frame.pack( side = "top" , expand = True , fill = "x" )
        option_frame.pack( side = "left" , expand = True , fill = "x" )
        # load & save button
        for text , func in [ [ "save" , self.save ] , [ "load" , self.load ] ] :
            tkinter.ttk.Button( option_frame , text = self.lang[ text ] , command = func ).pack( side = "top" , expand = True , fill = "both" )
        # info text
        self.info = tkinter.scrolledtext.ScrolledText( self.root , relief = "ridge" , font = self.font )
        self.info.pack( side = "bottom" , expand = True , fill = "both" )
        self.print( cls = True )

if __name__ == "__main__" :
    root = main( forge )
    root.run()
