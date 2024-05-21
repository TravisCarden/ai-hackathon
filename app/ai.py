from langchain_aws import ChatBedrock
from langchain.prompts import ChatPromptTemplate, PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnablePassthrough

anthropic_claude_llm = ChatBedrock(
    region_name="us-east-1",
    model_id="anthropic.claude-3-sonnet-20240229-v1:0",
    model_kwargs={"temperature": 0.1}
)

question = r"""token.tree:\\n  path: '/token/tree'\\n  defaults:\\n    _controller: '\\\\Drupal\\\\token\\\\Controller\\\\TokenTreeController::outputTree'\\n  requirements:\\n    _csrf_token: 'TRUE'\\n\\ntoken.flush_cache:\\n  path: '/token/flush-cache'\\n  defaults:\\n    _controller: '\\\\Drupal\\\\token\\\\Controller\\\\TokenCacheController::flush'\\n  requirements:\\n    _permission: 'flush caches'\\n    _csrf_token: 'TRUE'\\n    _module_dependencies: 'admin_menu'""";

answer = r"""```php\\n<?php\\n\\nnamespace Drupal\\\\Tests\\\\token\\\\Functional;\\n\\nuse Drupal\\\\block\\\\Entity\\\\Block;\\nuse Drupal\\\\node\\\\Entity\\\\Node;\\nuse Drupal\\\\node\\\\Entity\\\\NodeType;\\nuse Drupal\\\\Tests\\\\BrowserTestBase;\\nuse Drupal\\\\Tests\\\\system\\\\Functional\\\\Cache\\\\AssertPageCacheContextsAndTagsTrait;\\n\\n/**\\n * Tests URL tokens.\\n *\\n * @group token\\n */\\nclass UrlTest extends BrowserTestBase {{\\n\\n  use AssertPageCacheContextsAndTagsTrait;\\n\\n  /**\\n   * The first testing node.\\n   *\\n   * @var \\\\Drupal\\\\node\\\\NodeInterface\\n   */\\n  protected $node1;\\n\\n  /**\\n   * The second testing node.\\n   *\\n   * @var \\\\Drupal\\\\node\\\\NodeInterface\\n   */\\n  protected $node2;\\n\\n  /**\\n   * {{@inheritdoc}}\\n   */\\n  protected static $modules = ['node', 'token', 'block'];\\n\\n  /**\\n   * {{@inheritdoc}}\\n   */\\n  protected $defaultTheme = 'stark';\\n\\n  /**\\n   * {{@inheritdoc}}\\n   */\\n  protected function setUp(): void {{\\n    parent::setUp();\\n\\n    $node_type = NodeType::create(['type' => 'article', 'name' => 'Article']);\\n    $node_type->save();\\n\\n    $this->node1 = Node::create([\\n      'type' => 'article',\\n      'title' => 'Test Node 1',\\n    ]);\\n    $this->node1->save();\\n\\n    $this->node2 = Node::create([\\n      'type' => 'article',\\n      'title' => 'Test Node 2',\\n    ]);\\n    $this->node2->save();\\n\\n  }}\\n\\n  /**\\n   * Creates a block with token for title and tests cache contexts.\\n   *\\n   * @throws \\\\Behat\\\\Mink\\\\Exception\\\\ElementHtmlException\\n   * @throws \\\\Drupal\\\\Core\\\\Entity\\\\EntityStorageException\\n   */\\n  public function testBlockUrlTokenReplacement() {{\\n\\n    $node1_url = $this->node1->toUrl();\\n    $node2_url = $this->node2->toUrl();\\n\\n    // Using a @dataprovider causes repeated database installations and takes a\\n    // very long time.\\n    $tests = [];\\n    $tests[] = [\\n      'token' => 'prefix_[current-page:url:path]_suffix',\\n      'expected1' => 'prefix_/' . $node1_url->getInternalPath() . '_suffix',\\n      'expected2' => 'prefix_/' . $node2_url->getInternalPath() . '_suffix',\\n      // A path can only be generated from a routed path.\\n      'expected3' => 'prefix_/_suffix',\\n    ];\\n    $tests[] = [\\n      'token' => 'prefix_[current-page:url]_suffix',\\n      'expected1' => 'prefix_' . $node1_url->setAbsolute()->toString() . '_suffix',\\n      'expected2' => 'prefix_' . $node2_url->setAbsolute()->toString() . '_suffix',\\n      'expected3' => 'prefix_' . $this->getAbsoluteUrl('does-not-exist') . '_suffix',\\n    ];\\n\\n    // Place a standard block and use a token in the label.\\n    $edit = [\\n      'id' => 'token_url_test_block',\\n      'label' => 'label',\\n      'label_display' => TRUE,\\n    ];\\n    $this->placeBlock('system_powered_by_block', $edit);\\n    $block = Block::load('token_url_test_block');\\n\\n    $assert_session = $this->assertSession();\\n\\n    foreach ($tests as $test) {{\\n      // Set the block label.\\n      $block->getPlugin()->setConfigurationValue('label', $test['token']);\\n      $block->save();\\n\\n      // Go to the first node page and test that the token is correct.\\n      $this->drupalGet($node1_url);\\n      $assert_session->elementContains('css', '#block-token-url-test-block', $test['expected1']);\\n\\n      // Go to the second node page and check that the block title has changed.\\n      $this->drupalGet($node2_url);\\n      $assert_session->elementContains('css', '#block-token-url-test-block', $test['expected2']);\\n\\n      // Test the current page url on a 404 page.\\n      $this->drupalGet('does-not-exist');\\n      $assert_session->statusCodeEquals(404);\\n      $assert_session->elementContains('css', '#block-token-url-test-block', $test['expected3']);\\n    }}\\n\\n\\n    // Can't do this test in the for loop above, it's too different.\\n    $block->getPlugin()->setConfigurationValue('label', 'prefix_[current-page:query:unicorns]_suffix');\\n    $block->save();\\n\\n    // Test the parameter token.\\n    $this->drupalGet($node1_url->setOption('query', ['unicorns' => 'fluffy']));\\n    $this->assertCacheContext('url.query_args');\\n    $assert_session->elementContains('css', '#block-token-url-test-block', 'prefix_fluffy_suffix');\\n\\n    // Change the parameter on the same page.\\n    $this->drupalGet($node1_url->setOption('query', ['unicorns' => 'dead']));\\n    $assert_session->elementContains('css', '#block-token-url-test-block', 'prefix_dead_suffix');\\n  }}\\n\\n}}\\n"""

TEMPLATE = """Hello AI,

Do not output anything apart from the test case PHP code. I have a Drupal module and I need comprehensive automated tests created for it. Based on this data, generate tests that cover the functionalities reflected in the code.

Use the following format:
Question: "routing file data here"
Answer: "PHP test cases here"

Consider the following testing aspects:

- Backend logic: Create PHPUnit tests for services, hooks, and other PHP-based logic.
- Frontend behavior: If the module includes frontend components, create JavaScript tests that validate the user interface and interactions.
- Other Drupal-specific functionality: Generate tests for configuration forms, permissions, user interactions, entity operations, and more.

Focus on implementing detailed tests with assertions and logic that thoroughly validate the module's correctness and robust functionalities.

Here are some examples of routing files and test cases which are in JSON format:
Question: """ + question + """
Answer: """ + answer + """

Question: {question}
"""

custom_prompt_template = PromptTemplate(
    input_variables=["question"], template=TEMPLATE
)

prompt = ChatPromptTemplate.from_template(TEMPLATE)
model = anthropic_claude_llm

chain = (
    {
        "question": RunnablePassthrough()
    }
    | prompt
    | model
    | StrOutputParser()
)

def invoke(data):
    chain = (
        {
            "question": RunnablePassthrough()
        }
        | prompt
        | model
        | StrOutputParser()
    )
    return chain.invoke(data)
