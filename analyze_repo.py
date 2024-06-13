import os
import argparse
import openai
import datetime

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
                    {"role": "system", "content": "You are a code analyzer."},
                    {"role": "user", "content": f"Analyze the following code file based on these requirements: {requirements}\n\n{content}"}
                ],
                max_tokens=500
            )
            # print("----------")
            # print("Response:")
            # print(response)
            # print("----------")
            # print("Response.choices[0]:")
            # print(response.choices[0])
            # print("Response.choices[0].message:")
            # print(response.choices[0].message)
            # print("Response.choices[0].message.content:")
            # print(response.choices[0].message.content)
            # print("----------")
            analysis_results.append((file_path, response.choices[0].message.content))
        except Exception as e:
            print(f"Error analyzing file {file_path}: {e}")
    
    return analysis_results

def calculate_grade(analysis_results):
    # Function to calculate the grade based on the analysis results
    try:
        total_score = sum([len(result[1]) for result in analysis_results])
        max_score = 1000  # Arbitrary max score for normalization
        grade = (total_score / max_score) * 100
        return min(grade, 100)  # Ensure grade does not exceed 100
    except Exception as e:
        print(f"Error calculating grade: {e}")
        return 0

def generate_report(note, grade, analysis_results):
    # Function to generate the markdown report
    try:
        report = f"# Analysis Report\n\n**Note:** {note}\n\n"
        report += f"**Grade:** {grade:.2f}/100\n\n"
        report += "## Detailed Analysis\n\n"
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
    System Components:
    - Upload the input file to S3 from the browser directly (do not send the file content directly to Lambda)
        o S3 path: [BucketName]/[InputFile].txt
    - Save the inputs and S3 path in DynamoDB FileTable via API gateway and Lambda Function
        o id : [1] // auto-generated id via nanoid
        o input_text: [InputText]
        o input_file_path: [BucketName]/[InputFile].txt
    - After the file is uploaded in S3 and added to DynamoDB, trigger a script run in a VM instance (EC2) via the DynamoDB Event in order to do:
    [script starts here]
    1. Create a new VM automatically
    2. Download the script from S3 to the VM (Upload the scripts to S3 via CDK or programmatically as the InputFile)
    3. Run the script in the VM
        a) Get the inputs from DynamoDB FileTable by id
        b) Download the input file from S3 [BucketName]/[InputFile].txt to the VM
        c) Append the retrieved input text to the downloaded input file and save it as [OutputFile].txt
            i. [OutputFile].txt content: "[File Content] : [InputText]"
        d) Upload the output file to S3
            i. S3 path: [BucketName]/[OutputFile].txt
        e) Save the outputs and S3 path in DynamoDB FileTable
            i. id : [1]
            ii. output_file_path: [BucketName]/[OutputFile].txt
    4. Terminate the VM automatically
    [script ends here]

    Basic requirements:
    - Use AWS CDK to manage AWS infrastructure (latest version, TypeScript)
    - Use AWS SDK JavaScript V3 for Lambda (latest version, not V2)
    - Do not put any AWS access key / credentials in your code. (not in code, not in env, follow AWS best practices)
    - No SSH and no hard-coded parameters.
    - Your parameter/variable names are reader-friendly.
    - Your txt file in S3 is not public.
    - Do not use any AWS Amplify backend.
    - Follow the AWS Best Practices.
    - After saving the inputs and S3 path in DynamoDB FileTable, your system will create a new VM (not a pre-provisioned VM) and trigger the script to run automatically with error handling.
    """
    
    try:
        repo_files = load_repo_files(args.repo_path)
        if not repo_files:
            raise ValueError(f"No files found in the repository path: {args.repo_path}")

        analysis_results = analyze_with_gpt(client, args.model, requirements, repo_files)
        if not analysis_results:
            raise ValueError("Analysis results are empty, possibly due to errors during the GPT API calls.")
        
        grade = calculate_grade(analysis_results)
        report = generate_report(args.note, grade, analysis_results)
        
        if not report:
            raise ValueError("Generated report is empty, possibly due to errors in the report generation process.")
        
        print(report)  # Print the report to the screen
        save_report(report.encode('utf-8'), args.note)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
