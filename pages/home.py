import streamlit as st

def show_home():
    
    # Read about GDG on Campus PUP
    st.header("About")
    about = '''
    **Google Developer Groups on Campus Polytechnic University of the Philippines**, or **GDG PUP** for brevity, is a student-driven  organization supported by Google Developers, focused on creating a collaborative environment for  students to develop their technical skills and grow professionally. Our mission is to bridge the gap between theoretical  knowledge and real-world application, fostering a culture of peer-to-peer learning and innovation.  

    Founded in 2022, GDG PUP has quickly grown into a vibrant, university-wide community committed to empowering students in the fields of software development, engineering, and technology. By providing access to Google’s developer tools and resources, we support members in creating impactful solutions and projects that address real-world problems.

    At GDG PUP, we believe in the power of collaboration, creativity, and continuous learning. Our organization aims to:

    - Empower students through technology and programming education.  
    - Promote creativity, problem-solving, and innovation.  
    - Nurture the development of meaningful technological solutions for communities.  
    - Bridge the divide between theory and practice, turning learning into tangible experiences.  

    As we continue to grow, we remain focused on creating a space where students can network, learn, and contribute to the development of technology that can make a difference.   GDG PUP is a place where every student can thrive, and we believe that together, we can achieve great things by shaping the future of technology, one project at a time.  
    '''
    st.markdown(about)
    # Read about Data and ML initiatives
    st.subheader("Data and ML initiatives")
    st.markdown('''
    The GDG On Campus PUP Data and ML System is a comprehensive web application designed to serve as the digital  infrastructure for the **Google Developer Group at the Polytechnic University of the Philippines**. This platform  facilitates student engagement with data science and machine learning initiatives through an intuitive interface built  on modern web technologies.
                ''')
    # View development team members
    st.subheader("Development Team")

    image_paths = [
        "static\\images\\jp.jpg",
        "static\\images\\jen.jpg",
        "static\\images\\ferry.png",
        "static\\images\\redd.jpg",
        "static\\images\\gavin.jpg",
    ]


    names = ["John Paul Curada", "Jen Patrick Nataba", "John Ferry Lagman", "Redd Lawrence Reyes", "John Gavin Deposoy"]


    cols = st.columns(5)

    for col, img_path, name in zip(cols, image_paths, names):
        with col:
            st.image(img_path, use_column_width=True)
            st.write(f"**{name}**")
        