import streamlit as st
import base64
from openai_config import GPT_calls
import html
import os

def get_image_path(filename):
    return os.path.join('images', filename)

def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()
    
def replace_image_paths(html_content, image_files):
    for image_file in image_files:
        image_path = get_image_path(image_file)
        base64_data = convert_image_to_base64(image_path)
        html_content = html_content.replace(f" ./images/{image_file}", f"data:image/webp;base64,{base64_data}")
    return html_content

GPT_call = GPT_calls(name = "GPT Summarizer", model = "gpt-3.5-turbo", stream = False)

def generate_html(layout_type, grid_type, include_cards, color_theme, show_hero, show_features, 
                  show_testimonials, show_pricing, show_contact, alert_library, show_models):
    print(layout_type, grid_type, include_cards, color_theme, show_hero, show_features, 
                  show_testimonials, show_pricing, show_contact, alert_library, show_models)
    try:
        text = f"""
        Using tailwind CSS< create a deatailed and beautifully styled HTML for a landing page with the following
        features:

        1. Logo and Navigation:
            - Logo should be well-placed according to the selected layout ({layout_type}).
            - The logo image source should be "./images/icon.webp" relative to the HTML file.
            - The navigation bar should be placed according to the selected layout, either on the top, left,
              right, or as a hamburger menu.
            - Ensure the navigation is fully response and functional.
            - Use modern design elements and animations to enhance user experience.
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
        
        if show_models:
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
                - Hero Section: {"Included" if show_hero else "Not Included"}
                - Features Section: {"Included" if show_features else "Not Included"}
                - Testimonials Section: {"Included" if show_testimonials else "Not Included"}
                - Pricing Section: {"Included" if show_pricing else "Not Included"}
                - Contacts Section: {"Included" if show_contact else "Not Included"}
                - Alerts: {alert_library if show_models else "Not Included"}
                - Modal Functionality: {"Included" if show_models else "Not Included"}

                Please ensure that the generated HTML does not include the sections above. 
                Do not create any sections or components that were not explicitly selected.

                return only HTML code
                """
        response_generator = GPT_call.chat(f"{text}\n {selected_features}", color="magenta")
        response_text = ''.join(response_generator)

        with open("index.html", "w") as f:
            f.write(response_text)

            return response_text
    except Exception as e:
            return f"An error occured: {str(e)}"

def get_html_download_link(html_content):
    b64 = base64.b64encode(html_content.encode()).decode()
    href = f"<ca href='data:file/html;base64,{b64}' downloads='landing_page.html'>Download HTML file</a>"
    return href

def main():
    st.set_page_config(page_title='Advanced Landing Page Generator', page_icon=':rocket:', layout='wide')

    st.title('Advanced Landing Page Generator')

    with st.sidebar:
        st.subheader("Navigation")
        new_layout = st.selectbox('Select Navigation Layout', ['Fixed Top', 'Fixed Side', 'Hambuger Menu'])

        st.subheader('Sections')
        section_grid = st.selectbox('Select Section Grid', ['1 Column', '2 Columns', '3 Columns'])

        st.subheader('Cards')
        card_layout = st.selectbox('Select Card Layout', ['No Cards', '2 Cards', '3 Cards', '4 Cards'])

        st.subheader('Color Theme')
        color_theme = st.selectbox('Select Color Theme', ['Light', 'Dark', 'Colorful'])

        st.subheader("Alerts")
        alert_library = st.selectbox("Select Alert library", ['iziToast', "SweetAlert2"])

    with st.form("landing_page_form"):
        st.subheader("Additional Options")
        show_hero = st.checkbox("Include Hero Section")
        show_features = st.checkbox("Include Features Section")
        show_testimonials = st.checkbox("Include Testimonials Section")
        show_pricing = st.checkbox("Include Pricing Section")
        show_contact = st.checkbox("Include Contact Section")
        show_models = st.checkbox("Include Models")
        submitted = st.form_submit_button("Generate Landing Page")

    image_files = ["icon.webp", "img1.webp", "img2.webp", "img3.webp", "img4.webp", "img5.webp", "img6.webp",
                   "img7.webp", "img8.webp"]
    
    if submitted:
        layout_type = new_layout.lower().replace(' ', '-')
        grid_type = section_grid.split()[0]
        include_cards = card_layout != "No Cards"

        with st.spinner("Generating landing page..."):
            html_content = generate_html(layout_type, grid_type, include_cards, color_theme, show_hero, show_features
                                         , show_testimonials, show_pricing, show_contact, alert_library, show_models)
            
        if "error occured" not in html_content:
            modified_html_content = replace_image_paths(html_content, image_files)
            encoded_html = html.escape(modified_html_content)
            iframe_code = f"""
                <iframe srcdoc="{encoded_html}" width="100%" height="600" frameborder="2" sandbox="allow-scripts"></iframe>"""

            st.subheader("Template Preview:")
            st.components.v1.html(iframe_code, width=None, height=600)

            st.subheader("Generated HTML Code")
            st.code(html_content, language="html")

            download_link = get_html_download_link(html_content)
            st.markdown(download_link, unsafe_allow_html=True)

        else:
            st.error(html_content)

if __name__ == "__main__":
    main()