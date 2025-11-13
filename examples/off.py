from waveshare_transparent_screen_driver.oled_driver import OLED_1in51

disp = OLED_1in51()
disp.Init()
disp.off()
print("OLED OFF")
