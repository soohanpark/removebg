class Removebg < Formula
  include Language::Python::Virtualenv

  desc "Remove backgrounds from images using rembg (U^2-Net/BiRefNet)"
  homepage "https://github.com/soohanpark/removebg"
  url "https://github.com/soohanpark/removebg/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "REPLACE_WITH_SHA256_OF_RELEASE_TARBALL"
  license "MIT"

  depends_on "python@3.12"

  # ---------------------------------------------------------------------------
  # Resource pins for click, rembg, Pillow, onnxruntime, and all transitive
  # dependencies are auto-generated. Do NOT hand-edit. Run:
  #
  #     ./packaging/homebrew/generate-resources.sh
  #
  # then paste the printed `resource ... do ... end` blocks here, replacing
  # the BEGIN_RESOURCES / END_RESOURCES markers below.
  # ---------------------------------------------------------------------------
  # BEGIN_RESOURCES
  # END_RESOURCES

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match "Usage:", shell_output("#{bin}/removebg --help")
  end
end
