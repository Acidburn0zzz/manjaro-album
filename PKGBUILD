
# Maintainer: Guillaume Benoit <guillaume@manjaro.org>

pkgname=album
pkgver=0.9
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
_git=no

getsource() {
  cd "$srcdir"
  msg "Connecting to GIT server...."

  if [ -d $1 ] ; then
    if [ "$_git" == "yes" ] ; then
       cd $1 && git pull origin master
    else
       cd $1 && git pull origin master && git checkout -b $pkgver
    fi
    msg "The local files are updated."
  else
    git clone $2 $1
    if [ "$_git" != "yes" ] ; then
       cd $1 && git checkout -b $pkgver $pkgver
    fi
  fi

  msg "GIT checkout done or server timeout"
}

build() {
  cd "$srcdir"
  getsource "album" "git://git.manjaro.org/core/album.git"
}
 
package() {
  cd "$srcdir/$pkgname"
  python setup.py install --root="$pkgdir/" --optimize=1
  #install -Dm755 "${srcdir}/$pkgname/gui/album.glade" "${pkgdir}/usr/share/album/album.glade"
  #install -Dm755 "${srcdir}/$pkgname/album-gui" "${pkgdir}/usr/bin/album-gui"
  install -Dm755 "${srcdir}/$pkgname/album-cli" "${pkgdir}/usr/bin/album-cli"
  install -Dm755 "${srcdir}/$pkgname/scripts/11_btrfs-snapshots" "${pkgdir}/etc/grub.d/11_btrfs-snapshots"
  install -Dm644 "${srcdir}/$pkgname/scripts/umountbootinsnapshot.service" "${pkgdir}/usr/lib/systemd/system/umountbootinsnapshot.service"
}

# vim:set ts=2 sw=2 et:
