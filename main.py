from fastapi import FastAPI, HTTPException
from schemas import Composer, Piece

import json

app = FastAPI()


with open('composers.json', 'r') as f:
    composer_data = json.load(f)
    
composer_list = []
for composer in composer_data:
    composer = Composer(name=composer["name"], composer_id=composer["composer_id"], home_country=composer["home_country"])
    composer_list.append(composer)
        
with open('pieces.json', 'r') as f:
    pieces_data = json.load(f)

pieces_list = []
for piece in pieces_data:
    piece = Piece(name=piece["name"], alt_name=piece["alt_name"], difficulty=piece["difficulty"], composer_id=piece["composer_id"])
    pieces_list.append(piece)
    

@app.get('/composers')
async def get_composers() -> list[Composer]:
    
    return composer_list


@app.get('/pieces')
async def get_pieces(composer_id: None | int = None):
    
    if composer_id is not None:
        return [piece for piece in pieces_list if piece.composer_id == composer_id]
            
    return pieces_list
    

@app.post('/composers')
async def create_composer(composer: Composer):
    
    for existing_composers in composer_list:
        if composer.composer_id == existing_composers.composer_id:
            raise HTTPException(status_code=400, detail="Composer ID already exists")
    
    composer_list.append(composer)
    return 'Composer created successfully'


@app.post('/pieces')
async def create_piece(piece: Piece):
    
    if not any(composer.composer_id == piece.composer_id for composer in composer_list):
        raise HTTPException(status_code=400, detail="Composer ID does not exist")
    
    if piece.difficulty < 1 or piece.difficulty > 10:
        return 'Difficulty not valid. Input a number between 1-10'
    
    pieces_list.append(piece)
    return 'Piece created successfully'
    

@app.put('/composers/{composer_id}')
async def update_composer(composer_id: int, updated_composer: Composer):
    
    for i, composer in enumerate(composer_list):
        if composer.composer_id == composer_id:
            if any(existing_composer.composer_id == updated_composer.composer_id and existing_composer.composer_id != composer_id for existing_composer in composer_list):
                raise HTTPException(status_code=400, detail="Composer ID already exists")
            composer_list[i] = updated_composer
            return updated_composer

    if any(existing_composer.composer_id == updated_composer.composer_id for existing_composer in composer_list):
        raise HTTPException(status_code=400, detail="Composer ID already exists")
    
    composer_list.append(updated_composer)
    return updated_composer

@app.put('/pieces/{piece_name}')
async def update_piece(piece_name: str, updated_piece: Piece):
    
    if updated_piece.difficulty < 1 or updated_piece.difficulty > 10:
        raise HTTPException(status_code=400, detail="Difficulty not valid. Input a number between 1-10")
    
    if not any(composer.composer_id == updated_piece.composer_id for composer in composer_list):
        raise HTTPException(status_code=400, detail='Composer ID not found')
    
    for i, piece in enumerate(pieces_list):
        if piece.name == piece_name:
            pieces_list[i] = updated_piece
            return updated_piece
    
    pieces_list.append(updated_piece)
    return updated_piece
    

@app.delete('/composers/{composer_id}')
async def delete_composer(composer_id: int):
    
    for composer in composer_list:
        if composer.composer_id == composer_id:
            composer_list.remove(composer)
            return 'Deleted successfully'
    
    raise HTTPException(status_code=404, detail='Composer not found')


@app.delete('/pieces/{piece_name}')
async def delete_piece(piece_name: str):
    
    for piece in pieces_list:
        if piece.name == piece_name:
            pieces_list.remove(piece)
            return 'Deleted successfully'
    
    raise HTTPException(status_code=404, detail='Piece not found')
    
     
    
    