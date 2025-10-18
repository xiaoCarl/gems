def print_intro():
    """Display the welcome screen with ASCII art."""
    # ANSI color codes
    LIGHT_BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"
    
    # Clear screen effect with some spacing
    print("\n" * 2)
    
    # Welcome box with light blue border
    box_width = 50
    welcome_text = "价值投资分析"
    padding = (box_width - len(welcome_text) - 2) // 2
    
    print(f"{LIGHT_BLUE}{'═' * box_width}{RESET}")
    print(f"{LIGHT_BLUE}║{' ' * padding}{BOLD}{welcome_text}{RESET}{LIGHT_BLUE}{' ' * (box_width - len(welcome_text) - padding - 2)}║{RESET}")
    print(f"{LIGHT_BLUE}{'═' * box_width}{RESET}")
    print()
    
    # ASCII art for GEMS in block letters (financial terminal style)
    gems_art = f"""{BOLD}{LIGHT_BLUE}
      
      Great Enterprises at Moderate Prices 
    
    ██████╗    ███████╗  ███╗   ███╗  ███████╗
    ██╔════╝   ██╔════╝  ████╗ ████║  ██╔════╝
    ██║  ███╗  █████╗    ██╔████╔██║  ███████╗
    ██║   ██║  ██╔══╝    ██║╚██╔╝██║  ╚════██║
    ╚██████╔╝  ███████╗  ██║ ╚═╝ ██║  ███████║
     ╚═════╝   ╚══════╝  ╚═╝     ╚═╝  ╚══════╝
    
              好生意，好价格，长期持有   
{RESET}"""
    
    print(gems_art)
    print()
    print("您的AI金融分析助手。")
    print("请提出任何问题。输入'exit'或'quit'退出。")
    print()

