import { Link } from "react-router-dom";

function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="page-shell">
        <div className="site-footer__main">
          <div className="site-footer__brand">
            <Link
              to="/"
              className="brand"
              aria-label="Weathif home"
            >
              <img
                src="/logo.png"
                alt=""
                className="brand__logo"
              />

              <span>Weathif</span>
            </Link>

            <p>
              Explore real environmental conditions,
              historical context and hypothetical climate
              scenarios through interactive data.
            </p>
          </div>

          <nav
            className="site-footer__nav"
            aria-label="Footer navigation"
          >
            <div>
              <span>Explore</span>

              <Link to="/">
                Home
              </Link>

              <Link to="/simulator">
                Simulator
              </Link>
            </div>

            <div>
              <span>Understand</span>

              <Link to="/methodology">
                Methodology
              </Link>

              <Link to="/technology">
                Technology
              </Link>
            </div>
          </nav>
        </div>

        <div className="site-footer__bottom">
          <p>
            © {currentYear} Weathif
          </p>

          <p>
            Exploratory climate software — not a weather
            warning or scientific forecasting service.
          </p>

          <p>
            A Git It Bunny project.
          </p>
        </div>
      </div>
    </footer>
  );
}

export default Footer;