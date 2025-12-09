from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import os
import sendgrid
from sendgrid.helpers.mail import Email, Mail, Content, To
import markdown
from pathlib import Path


class EmailInvestmentThesisInput(BaseModel):
    """Input for sending the investment thesis via email."""
    investment_thesis: Optional[str] = Field(
        default=None, 
        description="The investment thesis content (markdown format) to send via email. If not provided, reads from output/decision.md"
    )


class EmailTool(BaseTool):
    name: str = "Send investment thesis via email"
    description: str = (
        "This tool sends the investment thesis report via email. "
        "It reads the decision.md file from the output directory, converts it to HTML format, and sends it to the configured email address. "
        "You can also provide the investment thesis content directly as a parameter."
    )
    args_schema: Type[BaseModel] = EmailInvestmentThesisInput

    def _run(self, investment_thesis: Optional[str] = None) -> str:
        sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
        email_from = os.getenv("EMAIL_FROM")
        email_to = os.getenv("EMAIL_TO")
        
        if not sendgrid_api_key:
            return '{"error": "SENDGRID_API_KEY environment variable is not set"}'
        
        if not email_from or not email_to:
            return '{"error": "EMAIL_FROM or EMAIL_TO environment variable is not set"}'
        
        # Read investment thesis from file if not provided
        if not investment_thesis:
            decision_file = Path("output/decision.md")
            if decision_file.exists():
                investment_thesis = decision_file.read_text(encoding="utf-8")
            else:
                return '{"error": "Investment thesis content not provided and decision.md file not found"}'
        
        # Convert markdown to HTML
        html_body = markdown.markdown(
            investment_thesis,
            extensions=['extra', 'nl2br']
        )
        
        # Add basic HTML styling
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1, h2, h3 {{ color: #2c3e50; }}
                strong {{ color: #27ae60; }}
                ul, ol {{ margin: 10px 0; padding-left: 30px; }}
                li {{ margin: 5px 0; }}
            </style>
        </head>
        <body>
            {html_body}
        </body>
        </html>
        """
        
        subject = "StockPicker Investment Thesis Report"
        
        try:
            sg = sendgrid.SendGridAPIClient(api_key=sendgrid_api_key)
            from_email = Email(email_from)
            to_email = To(email_to)
            content = Content("text/html", html_content)
            mail = Mail(from_email, to_email, subject, content).get()
            
            response = sg.client.mail.send.post(request_body=mail)
            print(f"Email sent successfully. Status code: {response.status_code}")
            return '{"status": "success", "message": "Investment thesis sent via email"}'
        except Exception as e:
            print(f"Error sending email: {str(e)}")
            return f'{{"error": "Failed to send email: {str(e)}"}}'