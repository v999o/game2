import colors

screen_width = 160
screen_height = 280

background_image = 'game2images/g2field.png'
gamesquare_image = 'game2images/g2fieldsquare_v2.png'
capital_image = 'game2images/g2capital_new.png'
soldier_image = 'game2images/g2soldier.png'
fieldsquare_blue_image = 'game2images/g2fieldsquare_blue.png'
fieldsquare_red_image = 'game2images/g2fieldsquare_red.png'

frame_rate = 90

row_count = 6
brick_width = 60
brick_height = 20
brick_color = colors.RED1
offset_y = brick_height + 10

ball_speed = 3
ball_radius = 8
ball_color = colors.GREEN

paddle_width = 80
paddle_height = 20
paddle_color = colors.ALICEBLUE
paddle_speed = 6

status_offset_y = 5

text_color1 = colors.BLUE
text_color2 = colors.RED1
text_color3 = colors.BLACK
initial_lives = 1
lives_right_offset = 85
lives_offset = screen_width - lives_right_offset

balance_blue_offset = screen_width - 80
income_blue_offset = screen_width - 40
balance_red_offset = 5
income_red_offset = 40

font_name = 'Arial'
font_size = 20

effect_duration = 20

sounds_effects = dict(
    brick_hit='sound_effects/brick_hit.wav',
    effect_done='sound_effects/effect_done.wav',
    paddle_hit='sound_effects/paddle_hit.wav',
    level_complete='sound_effects/level_complete.wav',
)

message_duration = 2

button_text_color = colors.WHITE,
button_normal_back_color = colors.INDIANRED1
button_hover_back_color = colors.INDIANRED2
button_pressed_back_color = colors.INDIANRED3

menu_offset_x = 20
menu_offset_y = 300
menu_button_w = 80
menu_button_h = 50
