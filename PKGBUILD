
# Maintainer: Guillaume Benoit <guillaume@manjaro.org>

pkgname=album
pkgver=0.8
pkgrel=1
pkgdesc="A snapshot manager for the btrfs filesystem"
arch=(any)
url="https://git.manjaro.org/core/album"
license=('GPL')
depends=('python' 'btrfs-progs' 'grub-common' 'gtk3' 'python-gobject')
makedepends=('git')
options=(!emptydirs)
install=
source=()
_gitroot=git://git.manjaro.org/core/album.git
_gitname=$pkgname

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [[ -d "$_gitname" ]]; then
     cd "$_gitname" && git pull origin && git checkout -b $pkgver
     msg "The local files are updated."
  else
     git clone "$_gitroot" "$_gitname" && git checkout -b $pkgver
  fi

  msg "GIT checkout done or server timeout"
}
 
package() {
  cd "$srcdir/$pkgname"
  python setup.py install --root="$pkgdir/" --optimize=1
  install -Dm755 "${srcdir}/$pkgname/gui/album.glade" "${pkgdir}/usr/share/album/album.glade"
  install -Dm755 "${srcdir}/$pkgname/album-gui" "${pkgdir}/usr/bin/album-gui"
  install -Dm755 "${srcdir}/$pkgname/album-cli" "${pkgdir}/usr/bin/album-cli"
  install -Dm755 "${srcdir}/$pkgname/scripts/11_btrfs-snapshots" "${pkgdir}/etc/grub.d/11_btrfs-snapshots"
}

# vim:set ts=2 sw=2 et:
