def render_platform_images(screen: pygame.surface):
    global platform_manager
    temp_image = None

    image_path_dict = {
        "base": "Resources/Sprites/Sprite-normal_log.png",
        "horizontal": "Resources/Sprites/Sprite-moving_log.png",
        "falling": "Resources/Sprites/Sprite-falling_log.png",
        "disappearing": "Resources/Sprites/Sprite-breaking_log.png",
    }

    for plat in platform_manager.platform_list:

        temp_image = pygame.image.load(image_path_dict[plat.type])
        temp_image = pygame.transform.scale(temp_image, (plat.width, plat.height))
        screen.blit(temp_image, (plat.x, plat.y))
