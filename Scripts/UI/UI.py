from Scripts.Engine import draw_multiline_text, pygame

def check_button_buffs(event, buffs, buffs_pos, buffs_get,buffs_button_offset):
    if (-buffs[0].offset_button[0] + buffs_pos[0] < event.pos[0] < buffs_pos[0] + buffs[0].size_button[0] +
        buffs[0].offset_button[
            0]) and \
            (-buffs[0].offset_button[1] + buffs_pos[1] < event.pos[1] < buffs_pos[1] + buffs[0].size_button[1] +
             buffs[0].offset_button[1]):
        buffs_get[0].chose()
        return 0
    elif (-buffs[0].offset_button[0] + buffs_pos[0] + buffs[0].size_button[0] + buffs_button_offset < event.pos[0] <
          buffs_pos[0] +
          buffs[0].size_button[0] + buffs[0].size_button[0] + buffs_button_offset + buffs[0].offset_button[
              0]) and \
            (-buffs[0].offset_button[1] + buffs_pos[1] < event.pos[1] < buffs_pos[1] + buffs[0].size_button[1] +
             buffs[0].offset_button[1]):
        buffs_get[1].chose()
        return 0
    return 1

def notification_new_level(screen,pos):
    font = pygame.font.Font('assets/fonts/HarryPotterKudosEN-en.ttf', 50)
    draw_multiline_text(screen,'level up',font,pos,(117, 162, 200), (0,0,0), 4)