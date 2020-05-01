import os
import hashlib
import gzip
from addons import __ADDONS__

class Generator:
    """
        Generates a new addons.xml file from each addons addon.xml file
        and a new addons.xml.sha256 hash file. Must be run from the root of
        the checked-out repo. Only handles single depth folder structure.
    """
    def __init__( self ):
        # generate files
        self._generate_addons_file()
        self._generate_hash_file()
        # notify user
        print "Finished updating addons xml and sha256 files"

    def _generate_addons_file( self ):
        # final addons text
        addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"
        # loop thru and add each addons addon.xml file
        for addon in __ADDONS__:
            try:
                # skip any file or .git folder
                if ( not os.path.isdir( addon )): 
                    print "Addon %s does not exist" % addon
                    continue
                # create path
                _path = os.path.join( addon, "addon.xml" )
                # split lines for stripping
                xml_lines = open( _path, "r" ).read().splitlines()
                # new addon
                addon_xml = ""
                # loop thru cleaning each line
                for line in xml_lines:
                    # skip encoding format line
                    if ( line.find( "<?xml" ) >= 0 ): continue
                    # add line
                    addon_xml += unicode( line.rstrip() + "\n", "utf-8" )
                # we succeeded so add to our final addons.xml text
                addons_xml += addon_xml.rstrip() + "\n\n"
            except Exception, e:
                # missing or poorly formatted addon.xml
                print "Excluding %s for %s" % ( _path, e, )
        # clean and add closing tag
        addons_xml = addons_xml.strip() + u"\n</addons>\n"
        # save file
        f = gzip.open('tmp/addons.xml.gz', 'wb')
        f.write(addons_xml.encode("utf-8"))
        f.close()
        self._save_file( addons_xml.encode( "utf-8" ), file="tmp/addons.xml" )

    def _generate_hash_file( self ):
        try:
            # create a new sha256 hash
            m = hashlib.sha256( open( "tmp/addons.xml.gz" ).read() ).hexdigest()
            # save file
            self._save_file( m, file="tmp/addons.xml.sha256" )
        except Exception, e:
            # oops
            print "An error occurred creating addons.xml.sha256 file!\n%s" % ( e, )

    def _save_file( self, data, file ):
        try:
            # write data to the file
            open( file, "w" ).write( data )
        except Exception, e:
            # oops
            print "An error occurred saving %s file!\n%s" % ( file, e, )


if ( __name__ == "__main__" ):
    # start
    Generator()