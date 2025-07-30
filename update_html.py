import re, glob, os

CUSTOMER_NAV = """
<nav class="flex justify-between bg-background border-t border-divider absolute bottom-0 inset-x-0">
  <a href="customer-home.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/home.svg" class="mx-auto w-5" />Home</a>
  <a href="cart.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/shopping-cart.svg" class="mx-auto w-5" />Cart</a>
  <a href="order-history.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/clipboard-document-list.svg" class="mx-auto w-5" />Orders</a>
  <a href="profile.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/user-circle.svg" class="mx-auto w-5" />Profile</a>
  <a href="wallet.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/wallet.svg" class="mx-auto w-5" />Wallet</a>
</nav>"""

VENDOR_NAV = """
<nav class="flex justify-between bg-background border-t border-divider absolute bottom-0 inset-x-0">
  <a href="vendor-home.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/home.svg" class="mx-auto w-5" />Dash</a>
  <a href="item-list.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/squares-plus.svg" class="mx-auto w-5" />Items</a>
  <a href="order-list.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/clipboard-document-list.svg" class="mx-auto w-5" />Orders</a>
  <a href="vendor-wallet.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/wallet.svg" class="mx-auto w-5" />Wallet</a>
  <a href="issue-center.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/exclamation-circle.svg" class="mx-auto w-5" />Issues</a>
</nav>"""

VENDOR_FILES = {
    "add-item.html","bulk-upload.html","create-shop.html","edit-vendor-profile.html",
    "issue-center.html","item-list.html","mark-delivered.html","modify-order.html",
    "order-list.html","vendor-basic-onboarding.html","vendor-dashboard.html",
    "vendor-index.html","vendor-kyc.html","vendor-login.html","vendor-profile.html",
    "vendor-wallet.html","withdraw.html","vendor-home.html"
}

def hero_image(is_vendor: bool) -> str:
    url = "https://source.unsplash.com/featured/?store" if is_vendor else "https://source.unsplash.com/featured/?shopping"
    return f'<img src="{url}" class="w-full h-40 object-cover rounded mb-4" />'

for path in glob.glob("**/*.html", recursive=True):
    filename = os.path.basename(path)
    is_vendor = filename in VENDOR_FILES
    nav = VENDOR_NAV if is_vendor else CUSTOMER_NAV
    with open(path, "r") as f:
        html = f.read()

    html = re.sub(r'<nav class="[^>]*bottom-0[^>]*>[\s\S]*?</nav>', '', html)
    html = re.sub(r'\s*<div class="w-\[390px\][^>]*>\s*', '', html)
    html = re.sub(r'</div>\s*</body>', '</body>', html)

    body_pattern = re.compile(r'<body[^>]*>')
    html = body_pattern.sub('<body class="min-h-screen bg-background-soft flex flex-col items-center">\n  <div class="w-[390px] max-w-full min-h-screen bg-background shadow-elevated flex flex-col relative">', html, count=1)
    html = re.sub(r'(</main>)', r'\1\n' + nav, html, count=1)
    html = re.sub(r'</body>', '</div>\n</body>', html, count=1)
    html = re.sub(r'(<main[^>]*>)', r'\1\n    ' + hero_image(is_vendor), html, count=1)

    with open(path, "w") as f:
        f.write(html)
