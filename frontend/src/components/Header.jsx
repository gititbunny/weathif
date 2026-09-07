import { useEffect, useState } from "react";
import {
  Link,
  NavLink,
  useLocation,
} from "react-router-dom";

function Header() {
  const [menuOpen, setMenuOpen] = useState(false);

  const location = useLocation();

  /* Close menu when route changes */
  useEffect(() => {
    setMenuOpen(false);
  }, [location.pathname]);

  /* Close menu with Escape key */
  useEffect(() => {
    const handleEscape = (event) => {
      if (event.key === "Escape") {
        setMenuOpen(false);
      }
    };

    window.addEventListener(
      "keydown",
      handleEscape
    );

    return () => {
      window.removeEventListener(
        "keydown",
        handleEscape
      );
    };
  }, []);

  /* Prevent page scrolling while menu is open */
  useEffect(() => {
    if (menuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [menuOpen]);

  return (
    <header
      className={`site-header ${
        menuOpen
          ? "site-header--menu-open"
          : ""
      }`}
    >
      <div className="site-header__inner">
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

        <nav
          className="site-nav"
          aria-label="Primary navigation"
        >
          <NavLink to="/">
            Home
          </NavLink>

          <NavLink to="/simulator">
            Simulator
          </NavLink>

          <NavLink to="/methodology">
            Methodology
          </NavLink>

          <NavLink to="/technology">
            Technology
          </NavLink>
        </nav>

        <div className="site-header__actions">
          <Link
            to="/simulator"
            className="header-cta"
          >
            Explore climate
          </Link>

          <button
            type="button"
            className={`mobile-nav-toggle ${
              menuOpen
                ? "mobile-nav-toggle--open"
                : ""
            }`}
            aria-label={
              menuOpen
                ? "Close navigation menu"
                : "Open navigation menu"
            }
            aria-expanded={menuOpen}
            aria-controls="mobile-navigation"
            onClick={() =>
              setMenuOpen(
                (current) => !current
              )
            }
          >
            <span />
            <span />
          </button>
        </div>
      </div>

      {menuOpen && (
        <nav
          id="mobile-navigation"
          className="mobile-nav"
          aria-label="Mobile navigation"
        >
          <div className="mobile-nav__inner">
            <div className="mobile-nav__top">
              <span>
                Navigate Weathif
              </span>

              <span>
                Climate exploration
              </span>
            </div>

            <div className="mobile-nav__links">
              <NavLink to="/">
                <span>
                  01
                </span>

                <strong>
                  Home
                </strong>

                <small>
                  Discover Weathif
                </small>
              </NavLink>

              <NavLink to="/simulator">
                <span>
                  02
                </span>

                <strong>
                  Simulator
                </strong>

                <small>
                  Explore a climate scenario
                </small>
              </NavLink>

              <NavLink to="/methodology">
                <span>
                  03
                </span>

                <strong>
                  Methodology
                </strong>

                <small>
                  Understand the science
                </small>
              </NavLink>

              <NavLink to="/technology">
                <span>
                  04
                </span>

                <strong>
                  Technology
                </strong>

                <small>
                  See how Weathif is built
                </small>
              </NavLink>
            </div>

            <div className="mobile-nav__footer">
              <span>
                Observe
              </span>

              <span>
                Compare
              </span>

              <span>
                Simulate
              </span>
            </div>
          </div>
        </nav>
      )}
    </header>
  );
}

export default Header;