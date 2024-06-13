import os
import argparse
import openai
import datetime

sentences_file_analyzer = 1
system_prompt_file_analyzer = f"You are a code grader and analyzer. Evaluate if the code provided complies with the requirements and, based on that, suggest a possible grade out of 100 and give a succint analysis. Format each response in Markdown, in this manner: start with the suggested grade followed by a period and then an evaluation that is at the very most {sentences_file_analyzer} sentence long. Always start your evaluation with a numeric grade and a period. Do not repeat code nor the requirements. Example output: **100/100** The code provided meets the requirements by uploading the file to S3 and saving the input in DynamoDB. "

sentences_whole_evaluation = 4
system_prompt_for_whole_evaluation = f"You are a grader, expert in grading code. You are tasked with evaluating a repo. You will be provided individual analysis for each of the files in the repo. Look at the analysis provided to you and generate a grade out of 100 based on the analysis. The analysis should be based on the requirements provided to you. The grade should be a number between 0 and 100. The analysis should be at the very most  {sentences_whole_evaluation} sentences long and formatted using markdown."

def is_binary_file(file_path):
    # Function to check if a file is binary
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
        return False
    except Exception as e:
        print(f"Error checking if file is binary {file_path}: {e}")
        return True

def load_repo_files(repo_path):
    # Function to load all files from the local git repo
    files_content = {}
    try:
        for root, _, files in os.walk(repo_path):
            if '.git' in root:
                continue
            for file in files:
                if file == '.gitignore':
                    continue
                file_path = os.path.join(root, file)
                if is_binary_file(file_path):
                    continue
                try:
                    with open(file_path, 'r') as f:
                        files_content[file_path] = f.read()
                except Exception as e:
                    print(f"Error reading file {file}: {e}")
    except Exception as e:
        print(f"Error walking through the repo path {repo_path}: {e}")
    return files_content

def analyze_with_gpt(client, model, requirements, files_content):
    # Function to analyze the files using GPT API
    analysis_results = []
    for file_path, content in files_content.items():
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt_file_analyzer},
                    {"role": "user", "content": f"Analyze the following code file based on these requirements: {requirements}\n\n{content}"}
                ],
                max_tokens=500
            )
            analysis_results.append((file_path, response.choices[0].message.content))
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
    
    return analysis_results

def analyze_results_with_gpt(client, model, requirements, results):
    # Function to analyze the results using GPT API

    results_concatenated = [f"{result[0]}: {result[1]}" for result in results]
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt_file_analyzer},
                {"role": "user", "content": f"Generate an evaluation based on these requirements: {requirements}.\n\n These are the individual evaluations per file: {results_concatenated}"}
            ],
            max_tokens=1000
        )
        final_result = response.choices[0].message.content
    except Exception as e:
        print(f"Error analyzing result: {e}")

    return final_result

def generate_final_evaluation(client, model, requirements, analysis_results):
    try:
        final_analysis = analyze_results_with_gpt(client, model, requirements, analysis_results)
        return final_analysis
    except Exception as e:
        print(f"Error generating final analysis: {e}")
        return 0

def generate_report(note, final_evaluation, analysis_results):
    # Function to generate the markdown report
    try:
        report = f"# Analysis Report\n\n**Note:** {note}\n\n"
        report += f"**Final evaluation:**\n\n {final_evaluation}\n\n"
        report += "## File by File Analysis\n\n"
        for file_path, analysis in analysis_results:
            report += f"### {file_path}\n{analysis}\n\n"
        return report
    except Exception as e:
        print(f"Error generating report: {e}")
        return ""

def save_report(report, note):
    # Function to save the report as a markdown file
    try:
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_filename = f"reports/report-{note}-{now}.md"
        os.makedirs(os.path.dirname(report_filename), exist_ok=True)
        with open(report_filename, 'wb') as f:
            f.write(report)
        print(f"Report saved to {report_filename}")
    except Exception as e:
        print(f"Error saving report: {e}")

def main():
    parser = argparse.ArgumentParser(description="Analyze a local git repo using GPT API")
    parser.add_argument("--endpoint", type=str, default="https://api.openai.com/v1",
                        help="Custom OpenAI endpoint URL (optional)")
    parser.add_argument("--model", type=str, default="gpt-4", help="GPT model to use (default: GPT-4)")
    parser.add_argument("--note", type=str, required=True, help="Note to include in the top of the report")
    parser.add_argument("--repo_path", type=str, required=True, help="Path to the local git repository")
    parser.add_argument("--api_key", type=str, required=False, help="OpenAI API key (optional)")

    args = parser.parse_args()

    api_key = args.api_key if args.api_key else os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key must be provided either as an argument or in the OPENAI_API_KEY environment variable.")

    client = openai.Client(api_key=api_key, base_url=args.endpoint)

    requirements = """

    **System Components:**

    1. **File Upload to S3:**
    - Upload the input file to S3 directly from the browser.
    - Do not send the file content directly to Lambda.
    - S3 path format: `[BucketName]/[InputFile].txt`.

    2. **Save Inputs and S3 Path in DynamoDB:**
    - Use API Gateway and a Lambda function to save the inputs and S3 path.
    - DynamoDB FileTable structure:
        - `id`: Auto-generated ID using nanoid.
        - `input_text`: The input text.
        - `input_file_path`: S3 path of the input file, `[BucketName]/[InputFile].txt`.

    3. **Trigger Script on VM Instance:**
    - After the file is uploaded to S3 and the information is added to DynamoDB, trigger a script run in an EC2 VM instance via a DynamoDB Event.
    - Script Workflow:
        1. Automatically create a new VM.
        2. Download the script from S3 to the VM (scripts should be uploaded to S3 using CDK or programmatically as the InputFile).
        3. Run the script in the VM:
            a) Retrieve inputs from DynamoDB FileTable using the ID.
            b) Download the input file from S3 (`[BucketName]/[InputFile].txt`) to the VM.
            c) Append the retrieved input text to the downloaded input file and save it as `[OutputFile].txt`.
            - `[OutputFile].txt` content: `"[File Content] : [InputText]"`.
            d) Upload the output file to S3.
            - S3 path: `[BucketName]/[OutputFile].txt`.
            e) Save the outputs and S3 path in DynamoDB FileTable.
            - `id`: The same ID.
            - `output_file_path`: S3 path of the output file, `[BucketName]/[OutputFile].txt`.
        4. Automatically terminate the VM.

    **Other Requirements:**

    - Do not include any AWS access keys or credentials in your code. Follow AWS best practices for security.
    - Use AWS CDK to manage AWS infrastructure (latest version, TypeScript).
    - The txt file in S3 should not be publicly accessible.
    - Do not include any AWS access keys or credentials in your code. Follow AWS best practices for security.
    - Do not use AWS Amplify backend.
    - Follow AWS Best Practices.
    - Use AWS SDK JavaScript V3 for Lambda (latest version, not V2).
    - Ensure that after saving the inputs and S3 path in DynamoDB FileTable, a new VM is created (not a pre-provisioned one), and the script runs automatically with proper error handling.
    - Ensure parameter and variable names are reader-friendly.
    """
    
    try:
        repo_files = load_repo_files(args.repo_path)
        if not repo_files:
            raise ValueError(f"No files found in the repository path: {args.repo_path}")

        analysis_results = analyze_with_gpt(client, args.model, requirements, repo_files)
        if not analysis_results:
            raise ValueError("Analysis results are empty, possibly due to errors during the GPT API calls.")
        
        final_evaluation = generate_final_evaluation(client, args.model, requirements, analysis_results)
        report = generate_report(args.note, final_evaluation, analysis_results)
        
        if not report:
            raise ValueError("Generated report is empty, possibly due to errors in the report generation process.")
        
        print(report)  # Print the report to the screen
        save_report(report.encode('utf-8'), args.note)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
