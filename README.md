github-issues-to-bitbucket-converter
====================================

Export GitHub issues to the Bitbucket issue format.

Summary
--------

This command-line script uses the GitHub API to extract all issues from a GitHub repository and create a ZIP file that can be imported into BitBucket's issue tracker.

Works with both public and private repositories. Does not yet support mapping GitHub issue labels to BitBucket issue kinds/priorities, nor does it support mapping GitHub users to BitBucket users. Pull requests are welcomed.

See the requirements.txt file for dependencies.

Reference
---------

https://confluence.atlassian.com/display/BITBUCKET/Export+or+Import+Issue+Data
https://confluence.atlassian.com/pages/viewpage.action?pageId=330796872
