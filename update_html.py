import re, glob, os
customer_nav = """
<nav class="flex justify-between bg-background border-t border-divider absolute bottom-0 inset-x-0">
  <a href="customer-home.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/home.svg" class="mx-auto w-5" />Home</a>
  <a href="cart.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/shopping-cart.svg" class="mx-auto w-5" />Cart</a>
  <a href="order-history.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/clipboard-document-list.svg" class="mx-auto w-5" />Orders</a>
  <a href="profile.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/user-circle.svg" class="mx-auto w-5" />Profile</a>
  <a href="wallet.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/wallet.svg" class="mx-auto w-5" />Wallet</a>
</nav>"""

vendor_nav = """
<nav class="flex justify-between bg-background border-t border-divider absolute bottom-0 inset-x-0">
  <a href="vendor-home.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/home.svg" class="mx-auto w-5" />Dash</a>
  <a href="item-list.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/squares-plus.svg" class="mx-auto w-5" />Items</a>
  <a href="order-list.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/clipboard-document-list.svg" class="mx-auto w-5" />Orders</a>
  <a href="vendor-wallet.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/wallet.svg" class="mx-auto w-5" />Wallet</a>
  <a href="issue-center.html" class="flex-1 py-3 text-center text-xs"><img src="https://unpkg.com/heroicons@2.1.0/24/exclamation-circle.svg" class="mx-auto w-5" />Issues</a>
</nav>"""

vendor_files = {
"add-item.html","bulk-upload.html","create-shop.html","edit-vendor-profile.html","issue-center.html","item-list.html","mark-delivered.html","modify-order.html","order-list.html","vendor-basic-onboarding.html","vendor-dashboard.html","vendor-index.html","vendor-kyc.html","vendor-login.html","vendor-profile.html","vendor-wallet.html","withdraw.html"}

for path in glob.glob("*.html"):
    nav = vendor_nav if path in vendor_files else customer_nav
    with open(path) as f:
        html = f.read()
    html = re.sub(r'<body class="[^"]*bg-background-soft[^"]*">', '<body class="min-h-screen bg-background-soft flex flex-col items-center">\n  <div class="w-[390px] max-w-full min-h-screen bg-background shadow-elevated flex flex-col relative">', html)
    html = re.sub(r'<nav class="[^"]*fixed bottom-0[\s\S]*?</nav>', '', html)
    html = re.sub(r'<footer class="[^"]*fixed bottom-0[\s\S]*?</footer>', '', html)
    html = html.replace('</main>', '</main>\n'+nav)
    html = html.replace('</body>', '</div>\n</body>')
    html = re.sub(r'(Phone Number.*?\n\s*)<input', r'\1<input value="9999999999"', html, flags=re.S)
    html = re.sub(r'(OTP.*?\n\s*)<input', r'\1<input value="123456"', html, flags=re.S)
    html = re.sub(r'(Name.*?\n\s*)<input', r'\1<input value="John Doe"', html, flags=re.S)
    html = re.sub(r'(Address.*?\n\s*)<input', r'\1<input value="221B Baker Street"', html, flags=re.S)
    html = re.sub(r'(Amount.*?\n\s*)<input', r'\1<input value="500"', html, flags=re.S)
    html = re.sub(r'(Bank Account.*?\n\s*)<input', r'\1<input value="XXXXXX1234"', html, flags=re.S)
    html = re.sub(r'<input(?![^>]*value=)', '<input value="Sample"', html)
    with open(path, 'w') as f:
        f.write(html)
