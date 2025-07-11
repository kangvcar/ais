class Ais < Formula
  desc "AI-powered terminal assistant for command analysis and learning"
  homepage "https://github.com/kangvcar/ais"
  url "https://github.com/kangvcar/ais/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "PLACEHOLDER_SHA256"
  license "MIT"
  head "https://github.com/kangvcar/ais.git", branch: "main"

  depends_on "python@3.12"

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      The AIS command-line tool has been installed as `ais`.
      
      To get started:
        ais --help
        ais ask "How do I use git?"
        ais config
      
      For shell integration (automatic error analysis):
        ais setup-shell
        source ~/.bashrc  # or ~/.zshrc
    EOS
  end

  test do
    assert_match "ais, version", shell_output("#{bin}/ais --version")
    assert_match "Usage:", shell_output("#{bin}/ais --help")
  end
end