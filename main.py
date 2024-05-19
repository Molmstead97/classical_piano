from fastapi import FastAPI, HTTPException, Query
from schemas import Composer, Piece
from typing import Optional

import json

app = FastAPI()


with open('composers.json', 'r') as f:
    composer_data = json.load(f)
    
composer_list = []
for composer in composer_data:
    composer_list.append(composer)
        
with open('pieces.json', 'r') as f:
    pieces_data = json.load(f)

pieces_list = []
for piece in pieces_data:
    pieces_list.append(piece)
    

@app.get('/composers')
async def get_composers() -> list[Composer]:
    
    return composer_list

@app.get('/pieces')
async def get_pieces(composer_id: Optional[int] = Query(None)):
    
    if composer_id is not None:
        return [piece for piece in pieces_list if piece['composer_id'] == composer_id]
            
    return pieces_list
    
@app.post('/composers')
async def create_composer(composer: Composer):
    
    for existing_composers in composer_list:
        if composer.composer_id == existing_composers['composer_id']:
            raise HTTPException(status_code=400, detail="Composer ID already exists")
    
    composer_list.append(composer)
    return 'Composer created successfully'

@app.post('/pieces')
async def create_piece(piece: Piece):
    
    if not any(composer['composer_id'] == piece.composer_id for composer in composer_list):
        raise HTTPException(status_code=400, detail="Composer ID does not exist")
    
    if piece.difficulty < 1 or piece.difficulty > 10:
        return 'Difficulty not valid. Input a number between 1-10'
    
    pieces_list.append(piece)
    return 'Piece created successfully'
    

@app.put('/composers/{composer_id}')
async def update_composer(composer_id: int, composer: Composer):
    
    for id, composer in enumerate(composer_list):
        if composer['composer_id'] == composer_id:
            composer_list[id] = composer
            return composer
    
    if any(composer['composer_id'] == composer.composer_id for composer in composer_list):
        raise HTTPException(status_code=400, detail="Composer ID already exists")
    
    composer_list.append(composer)
    return composer

@app.put('/pieces/{piece_name}')
async def update_piece(piece_name: str, piece: Piece):
    
    for name, piece in enumerate(pieces_list):
        if piece['name'] == piece_name:
            pieces_list[name] = piece
            return piece
    
    if any(piece['name'] == piece.name for piece in pieces_list):
        raise HTTPException(status_code=400, detail="piece ID already exists")
    
    pieces_list.append(piece)
    return piece
    

@app.delete('/composers/{composer_id}')
async def delete_composer(composer_id: int):
    
    for composer in composer_list:
        if composer['composer_id'] == composer_id:
            composer_list.remove(composer)
            return 'Deleted successfully'
    
    raise HTTPException(status_code=404, detail='Composer not found')

@app.delete('/pieces/{piece_name}')
async def delete_piece(piece_name: str):
    
    for piece in pieces_list:
        if piece['name'] == piece_name:
            pieces_list.remove(piece)
            return 'Deleted successfully'
    
    raise HTTPException(status_code=404, detail='Piece not found')
    
     
    
    