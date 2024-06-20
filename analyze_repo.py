import os
import argparse
import openai
import datetime

sentences_file_analyzer = 4
system_prompt_file_analyzer = f"You are a code grader and analyzer. You will be given the code of one of the files in a repo. Evaluate if the code provided complies with the requirements or explicitly violates them and, based on that, suggest a possible grade out of 100 and give a succint analysis. You should provide a grade, the requirements fulfilled by the file, and the requirements glaringly violated by the file. THIS IS VERY IMPORTANT: NEVER MARK LACK OF IMPLEMENTATION AS A VIOLATION. Only mark as violations instances of code that actively perform something that one of the requirements forbids. Example: If Requirement 55 is 'never use Chinese character in variables'. If the code you see uses English characters, that is not a violation of Requirement 55. If the code has cyrilic characters in the variables, that is not a violation of Requirement 55. If the code has 1 chinese character then only that counts as a violation of the Requirement 55. Another example: Requirement 67 is 'zip the uploaded file'. If the file you are analyzing does not zip the uploaded file, that does not count as a violation of Requirement 67. That is an omission and it is fine and should be ignored. Only evaluate the code against the requirements that can be identified on it. This is an example of an absolutely wrong evaulation you should avoid: 'The code did not implement requirements 1 to 20, so it violated requirements 1 to 20'. Never equate 'do not implement' with 'violation'. VERY IMPORTANT: LACK OF IMPLEMENTATION IS NEVER A VIOLATION. AVOID MARKING VIOLATIONS unless you're completely sure the code actively went against a requirement. LACK OF IMPLEMENTATION DOES NOT MEAN VIOLATION. And avoid grading the code for things it didn't do. If it does nothing, then it gets a 100/100 and zero violations. Format: each response should be in markdown, in this manner: start with the suggested grade followed by a period, a list of the requirements it implemented and violated, and then a general evaluation at most {sentences_file_analyzer} sentences long. Assume code is always visible so avoid rewriting or reprinting it. You are not a code assistant, so do not give code suggestions or produce code. Simply evaluate and grade. Refer to requirements by number, do not restate them. Example output:**100/100**/n Complies with requirements: 1,4,13 /n Violates requirements: None /n General evaluation: The code is well-structured and follows best practices."

sentences_whole_evaluation = 4
system_prompt_for_whole_evaluation = f"You are an expert in writing code grading reports. You are tasked with evaluating a repo. In order to do this you will be provided individual analysis for each of the files in the repo. Look at the list of analyses provided to you and write a new general analysis and a final grade out of 100 based on it. Your analysis should be based on the requirements provided to you. The grade should be a number between 0 and 100. Your analysis should be at the very most  {sentences_whole_evaluation} sentences long and formatted using markdown. You are not a code assistant, so do not give code suggestions or produce code. Simply evaluate and grade. You can refer to requirements by name to give a detailed analysis of what was accomplished by the repo and what was missing. Do not use a conversational tone, you are writing a document. Do not address anybody. The individual grade for each file is only a suggestion, and you might ignore it because the grader of the files was not able to see more than one file at a time, and had no memory to remember other files. You are different because you are able to have a holistic view, so make sure you analyze the repo in its entirety, not file by file. Do not provide grading per file, only provide a final grade. Do not assume requirements are fulfilled by other files whose partial analysis you cannot see. Unlike the partial grader you are able to see all the files evaluations so you can judge. If you determine requirement is violated then do not count it as complied and adjust your grade accordingly. Penalize each violation at least 15% off the final grade. Only base your analysis on what you can see. Also list what requirements were not met. Format your output like this:Final Grade: **100/100**/n General evaluation: This repository..."

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
                if file == '.gitignore' or file.upper() == '.env'.upper():
                    continue
                if file.upper() == 'README.md'.upper():
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

def load_requirements(file_path='specifications.txt'):
    try:
        with open(file_path, 'r') as file:
            requirements = [line.strip() for line in file.readlines()]
        return requirements
    except FileNotFoundError:
        print("Error: 'specifications.txt' file not found. Aborting.")
        exit(1)

def analyze_with_gpt(client, model, requirements, files_content):
    # Function to analyze the files using GPT API
    analysis_results = []
    for file_path, content in files_content.items():
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt_file_analyzer},
                    {"role": "user", "content": f"Analyze the following code file whose name is {file_path} based on these requirements: {requirements}\n\n{content}"}
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
                {"role": "user", "content": f"Generate a holistic evaluation of the whole project based on these requirements: {requirements}.\n\n These are the individual evaluations per file: {results_concatenated}"}
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

def generate_report(note, final_evaluation, requirements, analysis_results):
    # Function to generate the markdown report
    try:
        report = f"# Analysis Report\n\n**Note:** {note}\n\n"
        report += f"**Final evaluation:**\n\n {final_evaluation}\n\n"
        report += "## Requirements\n\n"
        for i, requirement in enumerate(requirements, 1):
            report += f"{requirement}\n"
        report += "## File by File Analysis\n\n"
        for file_path, analysis in analysis_results:
            report += f"### {file_path}\n{analysis}\n\n"
        report += "# Prompts used:\n\n"
        report += f"## File by File Analysis:\n\n{system_prompt_file_analyzer}\n\n"
        report += f"## Whole Evaluation:\n\n{system_prompt_for_whole_evaluation}\n\n"
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

    requirements = load_requirements()
    
    try:
        repo_files = load_repo_files(args.repo_path)
        if not repo_files:
            raise ValueError(f"No files found in the repository path: {args.repo_path}")

        analysis_results = analyze_with_gpt(client, args.model, requirements, repo_files)
        if not analysis_results:
            raise ValueError("Analysis results are empty, possibly due to errors during the GPT API calls.")
        
        final_evaluation = generate_final_evaluation(client, args.model, requirements, analysis_results)
        report = generate_report(args.note, final_evaluation, requirements, analysis_results)
        
        if not report:
            raise ValueError("Generated report is empty, possibly due to errors in the report generation process.")
        
        print(report)  # Print the report to the screen
        save_report(report.encode('utf-8'), args.note)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
