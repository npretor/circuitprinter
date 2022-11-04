from app import db

class Recipe(db.Model): 
    """
    A recipe contains: 
        (string) process_type
        (dict) process_parameters: allowable parmeters would be: 
            on_delay
            off_delay
            retract_height 
    """
    __tablename__ = 'recipes'
    name = db.Column(db.String(100)) 
    process_types = ['extrusion_silver_print', 'adhesive_dispense', 'cure','pick_and_place', 'inspect'] 

    def __repr__(self) -> str:
        return '<Recipe %r>' % self.name 

class Tool(db.Model):
    """
    A tool contains: 
        (string) name: name of the tool 
        (class) actions: possible actions the tool can take 
    """
    __tablename__ = 'tools'
    name = db.Column(db.String(200)) 

    def __repr__(self) -> str:
        return '<Tool %r>' % self.name 

class Process(db.Model):
    """
    A process contains: 
        (class) Tool: 
        (class) Recipe: 
        (string) name: 
        (string) artwork_path: path to unparsed artwork file, dxf, gerber, etc 
        (list) artwork: 
    """
    __tablename__ = 'processes'
    name = db.Column(db.String(200))
    artwork_path = db.Column(db.String(500)) 
    
    def __init__(self, name, artwork_path):
        self.name = name 
        self.artwork_path = artwork_path

    def __repr__(self) -> str:
        return '<Process %r>' % self.name 

