class Ais < Formula
  desc "智能终端助手 - AI-powered terminal assistant"
  homepage "https://github.com/kangvcar/ais"
  url "https://github.com/kangvcar/ais/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # 需要在实际发布时替换
  license "MIT"
  head "https://github.com/kangvcar/ais.git", branch: "main"

  depends_on "python@3.11"

  def install
    virtualenv_install_with_resources
  end

  test do
    # 基本功能测试
    assert_match "AIS", shell_output("#{bin}/ais --version")
    
    # 命令行参数测试
    assert_match "help", shell_output("#{bin}/ais --help")
  end
end