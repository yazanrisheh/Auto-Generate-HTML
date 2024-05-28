import streamlit as st
import base64
from openai_config import GPT_calls
import html
import os
import streamlit.components.v1 as components
from PIL import Image

def get_image_path(filename):
    return os.path.join('images', filename)

def convert_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except FileNotFoundError:
        print(f"Error: File not found: {image_path}")
        return None  # Or handle the error appropriately

def replace_image_paths(html_content, image_files):
    # Get the absolute path of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    for image_file in image_files:
        image_path = os.path.join(script_dir, "images", image_file)
        base64_data = convert_image_to_base64(image_path)
        if base64_data:  # Check if the image was found and converted
            html_content = html_content.replace(f" ./images/{image_file}", f"data:image/webp;base64,{base64_data}")
    return html_content

def convert_image_to_webp(image_path):
    """Converts an image to WebP format."""
    try:
        img = Image.open(image_path)
        webp_path = os.path.splitext(image_path)[0] + ".webp"
        img.save(webp_path, "webp")
        return webp_path
    except FileNotFoundError:
        print(f"Error: File not found: {image_path}")
        return None

def handle_logo_upload(logo_image):
    """Handles logo upload and conversion to WebP."""
    if logo_image:
        # Save the logo image
        logo_path = os.path.join("images", "icon.webp")
        with open(logo_path, "wb") as f:
            f.write(logo_image.read())
        # Convert logo to WebP if necessary
        if logo_image.name.lower().endswith((".jpg", ".jpeg", ".png")):
            convert_image_to_webp(logo_path)

GPT_call = GPT_calls(name = "GPT Summarizer", model = "gpt-3.5-turbo", stream = False)

def generate_html(layout_type, grid_type, include_cards, color_theme, show_hero, show_features, 
                  show_testimonials, show_pricing, show_contact, alert_library, show_modals, logo_image, topic):
    print(layout_type, grid_type, include_cards, color_theme, show_hero, show_features, 
                  show_testimonials, show_pricing, show_contact, alert_library, show_modals)
    try:
        text = f"""
        Using tailwind CSS, create a deatailed and beautifully styled HTML for a landing page with the following
        features:

        1. Logo and Navigation:
            - Logo should be well-placed according to the selected layout ({layout_type}).
            - The logo image source should be "./images/icon.webp" relative to the HTML file.
            - The navigation bar should be placed according to the selected layout, either on the top, left,
              right, or as a hamburger menu.
            - Ensure the navigation is fully response and functional.
            - Use modern design elements and animations to enhance user experience.

            Topic: {topic}
        """

        if show_hero:
            text += """

        2. Hero Section:
            - Include a clear and compelling headline.
            - Add a supportive headline.
            - Incorporate high-quality images or videos that are optimized for web.
            - The image source for the hero section should be "./images/img1.webp" relative to the HTML file.
            - Include prominent call-to-action (CTA) button(s) with hover effects.
            - Use modern design elements and animations to enhance user experience
        """
            
        if show_features:
            text += """

            3. Features Section:
                - Highlight the key benefits of the product or service.
                - Use bullet points or short paragraphs for clear articulation.
                - Incorporate relevant icons or images to visualize each feature.
                - The image sources for features section should be "./images/img2.webp", "./images/img3.webp", and
                so on, relative to the HTML file.
                """
            
        if show_testimonials:
            text += """

            4. Testimonials Section:
                - Include customer testimonials, quotes, or reviews
                - Display customer logos or avatars to build credibility.
                - The image sources for customer logos or avators should be ./images/img3.webp", "./images/img4.webp", and
                so on, relative to the HTML file.
                Ensure responseive design for optimal viewing on different devices.
                """
            
        if show_pricing:
            text += """

            5. Pricing Section:
                - Present pricing plans or packages clearly.
                - Highlight the features and benefits of each plan.
                - Include CTA buttons for each plan.
                """
            
        if show_contact:
            text += """

            6. Contact Section:
                - Provide a contact form for users to get in touch.
                - Include a relevant contact information (email, phone, address).
                - Optionally, include a map or location details.
                """
            
        text += f"""

        7. Visual Elements and Design:
            - Implement the selected color theme ({color_theme}) consistently throughout the page.
            - Use visually appealing and contracting colors to highlight important elements like CTAs.
            - Choose clear, readable fonts that align with the brand's identity.
            - Ensure ample whitespaces around elements to reduce clutter and improve readability.
            - Optimize images for fast loading times.

        8. Section Grid and Layout:
            - Arrange sections in a {grid_type}-column grid, ensuring responsiveness across devices.
            - If {include_cards}, incorporate card-based layouts within sections to showcase content effectively.
            """
        
        if show_modals:
            text += f"""

            9. Alerts and Models:
                - Implement {alert_library} alerts for important notifications or messages.
                - Include functional models for additional content or interactions.
                """
            
        text += """

            10. Trust Signals and Credibility:
                - Display any relevant security badges, certifications, or trust seals.
                - Include satisfaction guarantees or money-back guarantees if applicable.
                - Mention any notable media mentions, awards, or accolades.

            11. Footer:
                - Include important links to pages like About Us, FAQs, Terms & Conditions, and Privacy Policy.
                - Provide multiple ways to contact the business (email, phone, social media)
                - Include social media icons linked to the company's profiles.

            12. Responsiveness and Accessibility:
                - Ensure the landing page is fully responsive and looks great on all devices (desktop, tablet, mobile).
                - Implement accessibility best practices, such as proper heading structure, ARIA attributes, and
                keyboard navigation.

            13. SEO Optimization:
                - Include relevant meta tags (title, description) optimized for search engines.
                - Use appropriate header tags (H1, H2, etc..) for content hierarchy.
                - Optimize images with descriptive alt tags.

            14. Performance and Testing:
                - Optimize the page for fast loading speed.
                - Test the page across different devices and browsers for consistency.
                - Validate the HTML markup to ensure there are no errors.

            Please generate the HTML code for the landing page based on the provided specification. The code should
            be well-structured, properly indented, and free of any syntax errors. Ensure strict adherence to the
            guidelines mentioned above.

            Make sure every component and element is well-placed and sized, and implemented interactivity where
            required.
            Only provide the HTML code without any extra text or comments.
            """
        
        selected_features = f"""

            Selected Features:
                - Navigation Layout: {layout_type}
                - Section Grid: {grid_type} columns
                - Cards: {"Included" if include_cards else "Not Included"}
                - Color Theme: {color_theme}
                - Alerts: {alert_library if show_modals else "Not Included"}
                - Hero Section: {"Included" if show_hero else "Not Included"}
                - Features Section: {"Included" if show_features else "Not Included"}
                - Testimonials Section: {"Included" if show_testimonials else "Not Included"}
                - Pricing Section: {"Included" if show_pricing else "Not Included"}
                - Contacts Section: {"Included" if show_contact else "Not Included"}
                - Modal Functionality: {"Included" if show_modals else "Not Included"}

                Please ensure that the generated HTML does not include the sections above. 
                Do not create any sections or components that were not explicitly selected.

                return only HTML code
                """
        response_generator = GPT_call.chat(f"{text}\n {selected_features}", color="magenta")
        response_text = ''.join(response_generator)

        with open("index.html", "w", encoding="utf-8") as f:
            f.write(response_text)

            return response_text
    except Exception as e:
            return f"An error occured: {str(e)}"

def main():
    st.set_page_config(page_title='Advanced Landing Page Generator', page_icon=':rocket:', layout='wide')

    st.title('Advanced Landing Page Generator')

    with st.sidebar:
        st.subheader("Navigation")
        new_layout = st.selectbox('Select Navigation Layout', ['Fixed Top', 'Fixed Side', 'Hambuger Menu'], help="""
            **Fixed Top:** The navigation bar remains fixed at the top of the page as the user scrolls.
            **Fixed Side:** The navigation bar remains fixed to the side of the page as the user scrolls.
            **Hambuger Menu:** The navigation menu is hidden behind a hamburger icon and appears when clicked.
            
            **For more information on navigation layouts:**
            - **Fixed Top:** https://getbootstrap.com/docs/3.4/examples/navbar-fixed-top/
            - **Burger Menu:** https://www.weareconflux.com/en/blog/tab-bar-vs-hamburger-menu/
            """)

        st.subheader('Sections')
        section_grid = st.selectbox('Select Section Grid', ['1 Column', '2 Columns', '3 Columns'], help="""
            Choose the number of columns you want in your section layouts.
            
            **For more information on grid layouts:**
            - https://www.google.com/imgres?q=grid%20layouts%20in%20web%20design&imgurl=https%3A%2F%2Felementor.com%2Fcdn-cgi%2Fimage%2Ff%3Dauto%2Cw%3D800%2Ch%3D480%2Fhttps%3A%2F%2Felementor.com%2Fblog%2Fwp-content%2Fuploads%2Felementor%2Fthumbs%2Fblog-with-columns-ov9diww9hu5slrxftnyfnhf1irikmbftrz1kfs3r8k.png&imgrefurl=https%3A%2F%2Felementor.com%2Fblog%2Fgrid-design%2F&docid=V8w2R0Lz6YDL-M&tbnid=TxzkLpHmmQui3M&vet=12ahUKEwig__uL06-GAxWM8bsIHSpaCWIQM3oECGgQAA..i&w=720&h=426&hcb=2&ved=2ahUKEwig__uL06-GAxWM8bsIHSpaCWIQM3oECGgQAA
            """)

        st.subheader('Cards')
        card_layout = st.selectbox('Select Card Layout', ['No Cards', '2 Cards', '3 Cards', '4 Cards'], help="""
            Choose if you want to use card layouts within your sections to showcase content.
            
            **For more information on card layouts:**
            - https://dribbble.com/tags/web-ui-card
            """)

        st.subheader('Color Theme')
        color_theme = st.selectbox('Select Color Theme', ['Light', 'Dark', 'Colorful'], help="""
            Choose a color theme for your landing page.
            """)

        st.subheader("Alerts")
        alert_library = st.selectbox("Select Alert library", ['iziToast', "SweetAlert2"], help="""
            Select an alert library to use for notifications and messages.
            
            **For more information on the alert libraries:**
            - **SweetAlert2:** https://sweetalert2.github.io/#download
            - **iziToast:** https://onedev.net/post/925
            """)

    st.subheader("Input topic for yoru website")
    topic = st.text_input("Enter the topic name:", help="Enter the topic for your landing page, e.g., 'Financial Services', 'Tech Startup', 'Online Course', etc.")

    with st.form("landing_page_form"):
        st.subheader("Logo Upload")
        logo_image = st.file_uploader("Upload your logo", type=["png", "jpg", "jpeg", "webp"], help="Upload your logo for the landing page. Accepted formats: PNG, JPG, JPEG, WebP.")
        st.subheader("Additional Options")
        show_hero = st.checkbox("Include Hero Section", help="""
            A Hero section is a large, prominent section at the top of the landing page that introduces your product or service.
            
            **For more information on Hero sections:**
            - https://www.marketermilk.com/blog/hero-section-examples
            """)
        show_features = st.checkbox("Include Features Section", help="This section highlights the key benefits and functionalities of your product or service.")
        show_testimonials = st.checkbox("Include Testimonials Section", help="Showcase customer feedback and reviews to build trust and credibility.")
        show_pricing = st.checkbox("Include Pricing Section", help="Present your pricing plans or packages clearly.")
        show_contact = st.checkbox("Include Contact Section", help="Provide a contact form and information for users to get in touch.")
        show_modals = st.checkbox("Include Modals", help="Use modals for additional content or interactions, like signup forms or product demos.")
        # submitted = st.form_submit_button("Generate Landing Page")

        
        submitted = st.form_submit_button("Generate Landing Page")

    image_files = ["img1.webp", "img2.webp", "img3.webp", "img4.webp", "img5.webp", "img6.webp",
                   "img7.webp", "img8.webp"]
    
    if submitted:
        # Convert logo to WebP if necessary
        handle_logo_upload(logo_image)

        layout_type = new_layout.lower().replace(' ', '-')
        grid_type = section_grid.split()[0]
        if card_layout != "No Cards":
            include_cards = True
        else:
            include_cards = False


        with st.spinner("Generating landing page..."):
            html_content = generate_html(layout_type, grid_type, include_cards, color_theme, show_hero, show_features
                                         , show_testimonials, show_pricing, show_contact, alert_library, show_modals, logo_image, topic)
            
        if "error occured" not in html_content:
            modified_html_content = replace_image_paths(html_content, image_files)
            encoded_html = html.escape(modified_html_content)
            iframe_code = f"""
                <iframe srcdoc="{encoded_html}" width="100%" height="600" frameborder="2" sandbox="allow-scripts"></iframe>"""

            st.subheader("Template Preview:")
            st.components.v1.html(iframe_code, width=None, height=600)

            st.subheader("Generated HTML Code")
            st.code(html_content, language="html")



        else:
            st.error(html_content)

if __name__ == "__main__":
    main()