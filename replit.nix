{ pkgs }: {
  deps = [
    pkgs.python311
    pkgs.xorg.xvfb
    pkgs.xorg.xorgserver
  ];
}
