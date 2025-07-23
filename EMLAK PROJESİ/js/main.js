document.addEventListener('DOMContentLoaded', async function() {
    const container = document.getElementById('featured-listings');
    if (!container) return;

    const response = await fetch('/api/featured-listings');
    const listingsObj = await response.json();

    container.innerHTML = Object.entries(listingsObj).map(([listingKey, listing]) => {
        let imgUrl = '';
        if (listing.gorseller) {
            if (Array.isArray(listing.gorseller)) {
                const validImages = listing.gorseller.filter(url => url && typeof url === 'string' && url.trim() !== '');
                imgUrl = validImages.length > 0 ? validImages[0] : '';
            } else if (typeof listing.gorseller === 'object') {
                const values = Object.values(listing.gorseller).filter(url => url && typeof url === 'string' && url.trim() !== '');
                imgUrl = values.length > 0 ? values[0] : '';
            } else if (typeof listing.gorseller === 'string' && listing.gorseller.trim() !== '') {
                imgUrl = listing.gorseller;
            }
        }
        return `
            <div>
                ${imgUrl ? `<img src="${imgUrl}" alt="İlan Resmi" width="200" height="150">` : `<div style="width:200px;height:150px;background:#eee;">Resim Yok</div>`}
                <div><b>${listing.baslik || ''}</b></div>
                <div>${listing.fiyat ? listing.fiyat + ' TL' : ''}</div>
                <div>${listing.ilce || ''}, ${listing.il || ''}</div>
                <button onclick="window.location.href='ilan-detay2.html?id=${listingKey}'">Detay</button>
            </div>
        `;
    }).join('');
});