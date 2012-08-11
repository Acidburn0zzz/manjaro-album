
# Maintainer: Guillaume Benoit <guillaume@manjaro.org>

pkgname=album
pkgver=20120811
pkgrel=1
pkgdesc="A snapshot manager for the btrfs filesystem"
arch=(any)
url="https://git.manjaro.org/core/album"
license=('GPL')
depends=('python' 'btrfs-progs' 'grub-common')
makedepends=('git')
options=(!emptydirs)
install=
source=()

_gitroot=git://git.manjaro.org/core/album.git
_gitname=album

build() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [[ -d "$_gitname" ]]; then
    cd "$_gitname" && git pull origin
    msg "The local files are updated."
  else
    git clone "$_gitroot" "$_gitname"
  fi

  msg "GIT checkout done or server timeout"
}
 
package() {
  cd "$srcdir/$pkgname"
  python setup.py install --root="$pkgdir/" --optimize=1
}

# vim:set ts=2 sw=2 et:
