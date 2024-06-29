import pygame as pg

def load_frame_from_spritesheet_with_tileset_size(spritesheet, rows, columns, row, column):
    frame_width = spritesheet.get_width()/columns
    frame_height = spritesheet.get_height()/rows
    image = pg.Surface((frame_width, frame_height))
    image.fill((255,5,255))
    image.set_colorkey((255,5,255))
    image.blit(spritesheet, (0-column*frame_width, 0-row*frame_height))
    return image

def load_frame_from_spritesheet_with_tile_size(spritesheet, tile_width, tile_height, row, column):
    frame_width = tile_width
    frame_height = tile_height
    image = pg.Surface((frame_width, frame_height))
    image.fill((255,5,255))
    image.set_colorkey((255,5,255))
    image.blit(spritesheet, (0-column*frame_width, 0-row*frame_height))
    return image