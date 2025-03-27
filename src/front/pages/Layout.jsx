import { Outlet } from "react-router-dom/dist"
import ScrollToTop from "../components/ScrollToTop"
import { BrowserRouter, Route, Routes } from "react-router-dom/dist"
import { Navbar } from "../components/Navbar"
import { Footer } from "../components/Footer"
import { Home } from "./Home"
import { Signup } from "./Signup"
import { Login } from "./Login"
import { Private } from "./Private"

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const Layout = () => {
    return (
        <ScrollToTop>
            <Navbar />
            
            <Routes>
                <Route element={<Home />} path="/" />
                <Route element={<Signup />} path="/signup" />
                <Route element={<Login />} path="/login" />
                <Route element={<Private />} path="/private" />
            </Routes>

            <Footer />
        </ScrollToTop>
    )
}