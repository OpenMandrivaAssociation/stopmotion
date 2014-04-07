Summary:	An application for creating stopmotion animations
Name:		stopmotion
Version:	0.7.2
Release:	1
License:	GPLv2+
Group:		Video
Url:		http://stopmotion.bjoernen.com/
Source0:	http://developer.skolelinux.no/info/studentgrupper/2005-hig-stopmotion/project_management/webpage/releases/%{name}-%{version}.tar.gz
BuildRequires:	librsvg
BuildRequires:	qt4-linguist
BuildRequires:	inotifytools-devel
BuildRequires:	libtar-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(gamin)
BuildRequires:	pkgconfig(libxml-2.0)
BuildRequires:	pkgconfig(SDL_image)
BuildRequires:	pkgconfig(vorbis)
Requires:	vgrabbj

%description
Stopmotion is a free application for creating stop-motion animation movies.
The users will be able to create stop-motions from pictures imported from
a camera or from the harddrive, add sound effects and export the animation
to different video formats such as mpeg or avi.

%files
%doc README AUTHORS manual/
%{_bindir}/*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/%{name}/*
%{_iconsdir}/hicolor/*/apps/%{name}.png
%{_iconsdir}/%{name}.svg

#----------------------------------------------------------------------------

%prep
%setup -q

%build
lrelease translations/*
%qmake_qt4 PREFIX=%{_prefix}

%make
# Generate icons. The 48x48 one might be a bit ugly, but it'll have to do
convert graphics/stopmotion.png -resize 16x16 graphics/stopmotion-16.png
convert graphics/stopmotion.png -resize 48x48 graphics/stopmotion-48.png

%install
make install INSTALL_ROOT=%{buildroot}

# Install icons of various sizes
for s in 256 128 96 48 32 22 16 ; do
    mkdir -p %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps
    rsvg-convert -w ${s} -h ${s} \
    graphics/%{name}.svg -o \
    %{buildroot}%{_datadir}/icons/hicolor/${s}x${s}/apps/%{name}.png
done

