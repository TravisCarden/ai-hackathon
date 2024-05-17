_Note: File created by GPT-4-Turbo_

# Drupal Module Test Generation Prompt

## Purpose

This prompt is designed to guide an AI chat interface in generating comprehensive automated tests for a Drupal module based on provided module code. The tests include PHPUnit for backend functionality and, if applicable, JavaScript tests for frontend functionality, all written to the best of the AI's capabilities.

## Instructions for AI

Hello AI,

I have a Drupal module and I need comprehensive automated tests created for it. I'm providing you with JSON data that represents the structure and contents of the module's files. Based on this data, generate tests that cover the functionalities reflected in the code.

Consider the following testing aspects:

- Backend logic: Create PHPUnit tests for services, hooks, and other PHP-based logic.
- Frontend behavior: If the module includes frontend components, create JavaScript tests that validate the user interface and interactions.
- Other Drupal-specific functionality: Generate tests for configuration forms, permissions, user interactions, entity operations, and more.

Focus on implementing detailed tests with assertions and logic that thoroughly validate the module's correctness and robust functionalities. Here's the JSON data representing the module:

**[Paste JSON Data Here]**

Once the tests are written, output them in a JSON format that can be consumed by the `create_files.php` script for creating test files in the Drupal module directory.

---

When using this prompt, you would replace the `[Paste JSON Data Here]` section with the actual JSON data structure. This will guide the AI to understand that the generated tests should be complete and ready to validate the module's features, not merely placeholders or stubs.
