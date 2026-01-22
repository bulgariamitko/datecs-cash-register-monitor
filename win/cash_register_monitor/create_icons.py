"""
Script to create icon files for the Cash Register Monitor application
"""

from PIL import Image, ImageDraw
import os


def create_icon(color, filename, size=64):
    """Create a colored circle icon and save as ICO file"""
    # Create image with transparency
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Color mapping
    colors = {
        'green': (0, 180, 0, 255),      # Connected
        'red': (220, 0, 0, 255),        # Disconnected  
        'yellow': (255, 200, 0, 255),   # Checking
        'gray': (128, 128, 128, 255)    # Unknown/Idle
    }
    
    color_rgba = colors.get(color, colors['gray'])
    
    # Draw circle with border
    margin = 6
    border_width = 2
    
    # Draw border (darker version of main color)
    border_color = tuple(max(0, c - 60) if i < 3 else c for i, c in enumerate(color_rgba))
    draw.ellipse([margin-border_width, margin-border_width, 
                 size-margin+border_width, size-margin+border_width], 
                 fill=border_color)
    
    # Draw main circle
    draw.ellipse([margin, margin, size-margin, size-margin], fill=color_rgba)
    
    # Add a small highlight for 3D effect
    highlight_size = size // 4
    highlight_margin = margin + size // 6
    highlight_color = tuple(min(255, c + 40) if i < 3 else max(100, c) for i, c in enumerate(color_rgba))
    draw.ellipse([highlight_margin, highlight_margin, 
                 highlight_margin + highlight_size, highlight_margin + highlight_size], 
                 fill=highlight_color)
    
    # Save as ICO file with multiple sizes
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
    icons = []
    
    for icon_size in icon_sizes:
        resized = image.resize(icon_size, Image.Resampling.LANCZOS)
        icons.append(resized)
    
    # Create icons directory if it doesn't exist
    icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
    os.makedirs(icons_dir, exist_ok=True)
    
    # Save the ICO file
    ico_path = os.path.join(icons_dir, filename)
    icons[0].save(ico_path, format='ICO', sizes=[(img.width, img.height) for img in icons])
    
    print(f"Created {ico_path}")
    return ico_path


def main():
    """Create all icon files"""
    print("Creating icon files for Cash Register Monitor...")
    
    # Create icons for different states
    create_icon('green', 'connected.ico')
    create_icon('red', 'disconnected.ico') 
    create_icon('yellow', 'checking.ico')
    create_icon('gray', 'unknown.ico')
    
    print("All icon files created successfully!")
    
    # Also create a larger PNG version for the application
    image = Image.new('RGBA', (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Draw a more detailed application icon
    margin = 16
    
    # Main circle (blue/green gradient effect)
    colors = [(0, 120, 180, 255), (0, 180, 120, 255)]
    
    # Draw gradient-like effect with multiple circles
    for i, color in enumerate(colors):
        offset = i * 2
        draw.ellipse([margin + offset, margin + offset, 
                     128 - margin - offset, 128 - margin - offset], 
                     fill=color)
    
    # Add connection symbol (two small circles connected by line)
    symbol_size = 8
    line_width = 3
    
    # Left circle (computer)
    left_x = 128 // 2 - 20
    left_y = 128 // 2
    draw.ellipse([left_x - symbol_size, left_y - symbol_size,
                 left_x + symbol_size, left_y + symbol_size], 
                 fill=(255, 255, 255, 255))
    
    # Right circle (cash register)
    right_x = 128 // 2 + 20  
    right_y = 128 // 2
    draw.ellipse([right_x - symbol_size, right_y - symbol_size,
                 right_x + symbol_size, right_y + symbol_size], 
                 fill=(255, 255, 255, 255))
    
    # Connection line
    draw.line([left_x + symbol_size, left_y, right_x - symbol_size, right_y], 
              fill=(255, 255, 255, 255), width=line_width)
    
    # Save as PNG
    icons_dir = os.path.join(os.path.dirname(__file__), 'icons')
    png_path = os.path.join(icons_dir, 'app_icon.png')
    image.save(png_path, format='PNG')
    print(f"Created {png_path}")


if __name__ == "__main__":
    main()