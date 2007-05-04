%define	version 0.6.0
%define rel	3
%define	release	%mkrel %rel
%define Summary An application for creating stopmotion animations

Name:		stopmotion
Summary:	%{Summary}
Version:	%{version} 
Release:	%{release} 
Source0:	http://developer.skolelinux.no/info/studentgrupper/2005-hig-stopmotion/project_management/webpage/releases/%{name}-%{version}.tar.bz2
URL:		http://stopmotion.bjoernen.com/
Group:		Video
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
License:	GPL
BuildRequires:	SDL_image-devel 
BuildRequires:  libvorbis-devel
BuildRequires:  libxml2-devel 
BuildRequires:  libtar-devel 
BuildRequires:  qt4-devel
BuildRequires:  qt4-linguist 
BuildRequires:  ImageMagick
BuildRequires:  gamin-devel

%description
Stopmotion is a free application for creating stop-motion animation movies.
The users will be able to create stop-motions from pictures imported from
a camera or from the harddrive, add sound effects and export the animation
to different video formats such as mpeg or avi.

%prep
%setup -q

%build
# Wrong permissions
chmod -R a+r *
for a in `find ./manual/`; do if [ ! -d $a ]; then chmod 644 $a;else chmod 755 $a;fi;done
PATH=/usr/lib/qt4/bin:$PATH %configure	--with-html-dir=%{_datadir}/doc/%{name}-%{version}/manual
perl -pi -e "s#-pipe -O2#%{optflags}#g" Makefile
PATH=/usr/lib/qt4/bin:$PATH %make
# Generate icons. The 48x48 one might be a bit ugly, but it'll have to do
convert graphics/stopmotion.png -resize 16x16 graphics/stopmotion-16.png
convert graphics/stopmotion.png -resize 48x48 graphics/stopmotion-48.png

%install
rm -rf %{buildroot}

install -m755 stopmotion -D %{buildroot}%{_bindir}/%{name}
install -m644 stopmotion.desktop -D %{buildroot}%{_datadir}/applications/%{name}

install -m644 graphics/stopmotion.png -D %{buildroot}%{_iconsdir}/%{name}.png
install -m644 graphics/stopmotion-16.png -D %{buildroot}%{_miconsdir}/%{name}.png
install -m644 graphics/stopmotion-48.png -D %{buildroot}%{_liconsdir}/%{name}.png
install -m644 graphics/stopmotion.png -D %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
install -m644 graphics/stopmotion-16.png -D %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

mkdir -p %{buildroot}%{_menudir}
cat << EOF > %{buildroot}%{_menudir}/%{name}
?package(%{name}):command="%{name}"\
 icon="%{name}.png" needs="X11" section="Multimedia/Video"\
  title="Stopmotion" longtitle="%{Summary}" xdg="true"
EOF

desktop-file-install	--vendor="" \
			--remove-category="Application" \
			--add-category="Qt" \
			--add-category="Video" \
			--add-category="AudioVideoEditing" \
			--add-category="X-MandrivaLinux-Multimedia-Video" \
			--dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Localization.
# Uses a weird localization system, got to hardcode it *sigh* :)
/usr/lib/qt4/bin/lrelease stopmotion.pro
mkdir -p %{buildroot}%{_datadir}/%{name}/translations/
install -m644 ./translations/*.qm %{buildroot}%{_datadir}/%{name}/translations/

%post
%{update_menus}

%postun
%{clean_menus}

%clean 
rm -rf $%{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS manual/
%{_bindir}/*
%{_datadir}/applications/%{name}
%{_datadir}/%{name}/*
%{_menudir}/%{name}
%{_iconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_iconsdir}/hicolor/32x32/apps/%{name}.png
%{_iconsdir}/hicolor/16x16/apps/%{name}.png
