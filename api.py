# Fabio Leandro Lapuinka
# Rest API - MongoDB - BigData - Telemetria - versão 1

import unicodedata
import re
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

# Configuration (should be in settings or environment variables)
MONGO_URI = "mongodb://{user}:{password}@ds015942.mlab.com:15942/doutrina_agil"
DEMO_TOKEN = "DAWbiMVyDhNOhBOgs7vbFMhEIUrLSQ6o2FZea="
MIN_QUERY_LENGTH = 3
API_VERSION = "2"

def remove_accents(data):
    """Normalize and clean input string"""
    try:
        return data.encode('utf-8').strip().decode('utf-8')
    except (UnicodeEncodeError, UnicodeDecodeError):
        return data.strip()

def set_cors_headers(response):
    """Set CORS headers for API responses"""
    response.view = 'generic.json'
    response.headers.update({
        "Access-Control-Allow-Origin": '*',
        "Access-Control-Max-Age": 86400,
        "Access-Control-Allow-Headers": '*',
        "Access-Control-Allow-Methods": '*',
        "Access-Control-Allow-Credentials": 'true'
    })
    return response

def get_mongo_connection():
    """Create MongoDB connection using configured credentials"""
    uri = MONGO_URI.format(
        user=current.db_user, 
        password=current.db_password
    )
    return MongoClient(uri).get_default_database()

def validate_request(token, query):
    """Validate API request parameters"""
    if str(token) != DEMO_TOKEN:
        return "Invalid Demo Token"
    if len(str(query).strip()) < MIN_QUERY_LENGTH:
        return f"Invalid Query Size, minimum {MIN_QUERY_LENGTH} chars!"
    return None

def log_access(db, ip, query):
    """Log access to database"""
    try:
        db['acessos'].insert_one({
            'v': API_VERSION,
            'ip': ip,
            'query': query,
            'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    except ConnectionFailure:
        pass

def build_response(db, query_terms):
    """Build API response from database query"""
    books_col = db['books']
    doutrinas_col = db['doutrinas']
    
    # Process books
    books_data = []
    for book in books_col.find():
        books_data.append(
            f'{{"book_id":"{book["id"]}", "author":"{book["author"]}", "title":"{book["title"]}"}}'
        )
    
    # Process doutrinas
    doutrinas_data = []
    seen_ids = set()
    
    for term in query_terms:
        if len(term) < MIN_QUERY_LENGTH:
            continue
            
        for doc in doutrinas_col.find({
            'texto': {'$regex': term, '$options': 'i'}
        }):
            if doc['_id'] not in seen_ids:
                seen_ids.add(doc['_id'])
                doutrinas_data.append(
                    f'{{"book_id":"{doc["book_id"]}", "page":"{doc["page"]}", "texto":"{doc["texto"]}"}}'
                )
    
    # Prepare statistics
    stats = {
        'v': API_VERSION,
        'n': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'a': request.env.http_x_forwarded_for,
        'q': ' '.join(query_terms)
    }
    
    try:
        stats['t'] = str(db['estatisticas'].count_documents({}))
    except ConnectionFailure:
        stats['t'] = "0"
    
    return {
        'livros': books_data,
        'doutrinas': doutrinas_data,
        **stats
    }

@request.restful()
def find():
    response = set_cors_headers(response)
    
    def GET(*args, **vars):
        patterns = 'auto'
        parser = db.parse_as_rest(patterns, args, vars)
        if parser.status == 200:
            return dict(content=parser.response)
        raise HTTP(parser.status, parser.error)
    
    def POST(token, query):
        # Validate request
        if error := validate_request(token, query):
            return error
        
        # Process query
        cleaned_query = remove_accents(query)
        query_terms = list(set(re.findall(r'\S+', cleaned_query)))
        
        # Database operations
        try:
            db = get_mongo_connection()
            log_access(db, request.env.http_x_forwarded_for, query)
            response_data = build_response(db, query_terms)
            
            if not response_data['doutrinas']:
                return '{}'
                
            return ('{"livros":[' + ','.join(response_data['livros']) + 
                   '], "doutrinas":[' + ','.join(response_data['doutrinas']) + 
                   f'], "q":"{response_data["q"]}", "v":"{response_data["v"]}", ' +
                   f'"n":"{response_data["n"]}", "a":"{response_data["a"]}", ' +
                   f'"t":"{response_data["t"]}"}}')
        except ConnectionFailure:
            return '{"error":"Database connection failed"}'

    return dict(GET=GET, POST=POST)