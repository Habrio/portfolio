import os, re, glob

def load_icon(name):
    with open(f"icons/{name}.svg") as f:
        svg = f.read().strip()
    return svg

ICONS = {
    'home': load_icon('home'),
    'shopping-cart': load_icon('shopping-cart'),
    'clipboard-document-list': load_icon('clipboard-document-list'),
    'user-circle': load_icon('user-circle'),
    'wallet': load_icon('wallet'),
    'squares-plus': load_icon('squares-plus'),
    'exclamation-circle': load_icon('exclamation-circle'),
    'building-storefront': load_icon('building-storefront'),
    'shopping-bag': load_icon('shopping-bag'),
}

hero_pattern = re.compile(r'<img src="https://source\.unsplash\.com/featured/\?(?:shopping|store)" class="w-full h-40 object-cover rounded mb-4" />')
icon_pattern = re.compile(r'<img src="https://unpkg.com/heroicons@2\.1\.0/24/([a-z-]+)\.svg" class="([^"]*)" ?/?>')

h1_pattern = re.compile(r'<h1[^>]*>')
h2_pattern = re.compile(r'<h2[^>]*>')

button_blue = re.compile(r'bg-blue-600')
hov_blue = re.compile(r'hover:bg-blue-700')

bg_gray = re.compile(r'bg-gray-200')

for path in glob.glob('consumer/*.html') + glob.glob('vendor/*.html'):
    is_vendor = path.startswith('vendor')
    with open(path) as f:
        html = f.read()

    # replace hero images
    icon_name = 'building-storefront' if is_vendor else 'shopping-bag'
    hero_svg = ICONS[icon_name]
    hero_div = f'<div class="w-full h-40 flex items-center justify-center rounded mb-4 bg-background-soft">{hero_svg}</div>'
    html = hero_pattern.sub(hero_div, html)

    # replace heroicon imgs with inline svg
    def repl_icon(m):
        name = m.group(1)
        classes = m.group(2)
        svg = ICONS.get(name, '')
        if classes:
            svg = svg.replace('<svg ', f'<svg class="{classes}" ', 1)
        return svg
    html = icon_pattern.sub(repl_icon, html)

    # typography
    html = h1_pattern.sub('<h1 class="text-xl font-bold text-text-primary">', html)
    html = h2_pattern.sub('<h2 class="text-lg font-semibold">', html)

    # buttons
    primary = 'bg-accent' if is_vendor else 'bg-primary'
    dark = 'bg-accent-dark' if is_vendor else 'bg-primary-dark'
    html = button_blue.sub(primary, html)
    html = hov_blue.sub(f'hover:{dark}', html)
    html = bg_gray.sub('border border-divider', html)

    with open(path, 'w') as f:
        f.write(html)
