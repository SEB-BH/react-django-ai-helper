import { Link } from "react-router"


const Nav = (props) => {

    const handleSignOut = () => {
        localStorage.removeItem('token')
        props.setUser(null)
    }

    return (
        <nav>
            <Link className="nav-brand" to="/">HOOT</Link>
            { props.user ? (
                <ul>
                    <li>WELCOME, {props.user.username}!</li>
                    <li><Link to='/hoots'>HOOTS</Link></li>
                    <li><Link to='/hoots/new'>NEW HOOT</Link></li>
                    <li><Link to="/" onClick={handleSignOut}>SIGN OUT</Link></li>
                </ul>
            ) : (
            <ul>
                <li><Link to='/'>HOME</Link></li>
                <li><Link to='/sign-up'>SIGN UP</Link></li>
                <li><Link to='/sign-in'>SIGN IN</Link></li>
            </ul>
            ) }
        </nav>
    )
}

export default Nav
