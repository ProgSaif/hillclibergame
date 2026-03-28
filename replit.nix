{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.xorg.libX11
    pkgs.xorg.libXext
    pkgs.xorg.libXrender
    pkgs.xorg.libXtst
    pkgs.xorg.libXi
    pkgs.xorg.libXrandr
    pkgs.xorg.libXcursor
    pkgs.xorg.libXinerama
    pkgs.xorg.libXScrnSaver
    pkgs.xorg.xorgserver
    pkgs.xorg.xvfb
  ];
}
