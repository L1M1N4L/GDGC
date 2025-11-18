from nextcord.ext import commands
import nextcord
import random

class LeetCode(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # NeetCode 250 problems organized by category
        self.problems = {
            "Arrays & Hashing": [
                "Concatenation of Array", "Contains Duplicate", "Valid Anagram", "Two Sum",
                "Longest Common Prefix", "Group Anagrams", "Remove Element", "Majority Element",
                "Design HashSet", "Design HashMap", "Sort an Array", "Sort Colors",
                "Top K Frequent Elements", "Encode and Decode Strings", "Range Sum Query 2D Immutable",
                "Product of Array Except Self", "Valid Sudoku", "Longest Consecutive Sequence",
                "Best Time to Buy And Sell Stock II", "Majority Element II", "Subarray Sum Equals K",
                "First Missing Positive"
            ],
            "Two Pointers": [
                "Reverse String", "Valid Palindrome", "Valid Palindrome II", "Merge Strings Alternately",
                "Merge Sorted Array", "Remove Duplicates From Sorted Array", "Two Sum II Input Array Is Sorted",
                "3Sum", "4Sum", "Rotate Array", "Container With Most Water", "Boats to Save People",
                "Trapping Rain Water"
            ],
            "Sliding Window": [
                "Contains Duplicate II", "Best Time to Buy And Sell Stock", "Longest Substring Without Repeating Characters",
                "Longest Repeating Character Replacement", "Permutation In String", "Minimum Size Subarray Sum",
                "Find K Closest Elements", "Minimum Window Substring", "Sliding Window Maximum"
            ],
            "Stack": [
                "Baseball Game", "Valid Parentheses", "Implement Stack Using Queues", "Implement Queue using Stacks",
                "Min Stack", "Evaluate Reverse Polish Notation", "Asteroid Collision", "Daily Temperatures",
                "Online Stock Span", "Car Fleet", "Simplify Path", "Decode String", "Maximum Frequency Stack",
                "Largest Rectangle In Histogram"
            ],
            "Binary Search": [
                "Binary Search", "Search Insert Position", "Guess Number Higher Or Lower", "Sqrt(x)",
                "Search a 2D Matrix", "Koko Eating Bananas", "Capacity to Ship Packages Within D Days",
                "Find Minimum In Rotated Sorted Array", "Search In Rotated Sorted Array", "Search In Rotated Sorted Array II",
                "Time Based Key Value Store", "Split Array Largest Sum", "Median of Two Sorted Arrays",
                "Find in Mountain Array"
            ],
            "Linked List": [
                "Reverse Linked List", "Merge Two Sorted Lists", "Linked List Cycle", "Reorder List",
                "Remove Nth Node From End of List", "Copy List With Random Pointer", "Add Two Numbers",
                "Find The Duplicate Number", "Reverse Linked List II", "Design Circular Queue",
                "LRU Cache", "LFU Cache", "Merge K Sorted Lists", "Reverse Nodes In K Group"
            ],
            "Trees": [
                "Binary Tree Inorder Traversal", "Binary Tree Preorder Traversal", "Binary Tree Postorder Traversal",
                "Invert Binary Tree", "Maximum Depth of Binary Tree", "Diameter of Binary Tree", "Balanced Binary Tree",
                "Same Tree", "Subtree of Another Tree", "Lowest Common Ancestor of a Binary Search Tree",
                "Insert into a Binary Search Tree", "Delete Node in a BST", "Binary Tree Level Order Traversal",
                "Binary Tree Right Side View", "Construct Quad Tree", "Count Good Nodes In Binary Tree",
                "Validate Binary Search Tree", "Kth Smallest Element In a Bst", "Construct Binary Tree From Preorder And Inorder Traversal",
                "House Robber III", "Delete Leaves With a Given Value", "Binary Tree Maximum Path Sum",
                "Serialize And Deserialize Binary Tree"
            ],
            "Heap / Priority Queue": [
                "Kth Largest Element In a Stream", "Last Stone Weight", "K Closest Points to Origin",
                "Kth Largest Element In An Array", "Task Scheduler", "Design Twitter", "Single Threaded CPU",
                "Reorganize String", "Longest Happy String", "Car Pooling", "Find Median From Data Stream", "IPO"
            ],
            "Backtracking": [
                "Sum of All Subsets XOR Total", "Subsets", "Combination Sum", "Combination Sum II",
                "Combinations", "Permutations", "Subsets II", "Permutations II", "Generate Parentheses",
                "Word Search", "Palindrome Partitioning", "Letter Combinations of a Phone Number",
                "Matchsticks to Square", "Partition to K Equal Sum Subsets", "N Queens", "N Queens II",
                "Word Break II"
            ],
            "Tries": [
                "Implement Trie Prefix Tree", "Design Add And Search Words Data Structure",
                "Extra Characters in a String", "Word Search II"
            ],
            "Graphs": [
                "Island Perimeter", "Verifying An Alien Dictionary", "Find the Town Judge", "Number of Islands",
                "Max Area of Island", "Clone Graph", "Walls And Gates", "Rotting Oranges",
                "Pacific Atlantic Water Flow", "Surrounded Regions", "Open The Lock", "Course Schedule",
                "Course Schedule II", "Graph Valid Tree", "Course Schedule IV",
                "Number of Connected Components In An Undirected Graph", "Redundant Connection",
                "Accounts Merge", "Evaluate Division", "Minimum Height Trees", "Word Ladder"
            ],
            "Advanced Graphs": [
                "Path with Minimum Effort", "Network Delay Time", "Reconstruct Itinerary",
                "Min Cost to Connect All Points", "Swim In Rising Water", "Alien Dictionary",
                "Cheapest Flights Within K Stops", "Find Critical and Pseudo Critical Edges in Minimum Spanning Tree",
                "Build a Matrix With Conditions", "Greatest Common Divisor Traversal"
            ],
            "1-D Dynamic Programming": [
                "Climbing Stairs", "Min Cost Climbing Stairs", "N-th Tribonacci Number", "House Robber",
                "House Robber II", "Longest Palindromic Substring", "Palindromic Substrings", "Decode Ways",
                "Coin Change", "Maximum Product Subarray", "Word Break", "Longest Increasing Subsequence",
                "Partition Equal Subset Sum", "Combination Sum IV", "Perfect Squares", "Integer Break",
                "Stone Game III"
            ],
            "2-D Dynamic Programming": [
                "Unique Paths", "Unique Paths II", "Minimum Path Sum", "Longest Common Subsequence",
                "Last Stone Weight II", "Best Time to Buy And Sell Stock With Cooldown", "Coin Change II",
                "Target Sum", "Interleaving String", "Stone Game", "Stone Game II",
                "Longest Increasing Path In a Matrix", "Distinct Subsequences", "Edit Distance",
                "Burst Balloons", "Regular Expression Matching"
            ],
            "Greedy": [
                "Lemonade Change", "Maximum Subarray", "Maximum Sum Circular Subarray",
                "Longest Turbulent Subarray", "Jump Game", "Jump Game II", "Jump Game VII",
                "Gas Station", "Hand of Straights", "Dota2 Senate", "Merge Triplets to Form Target Triplet",
                "Partition Labels", "Valid Parenthesis String", "Candy"
            ],
            "Intervals": [
                "Insert Interval", "Merge Intervals", "Non Overlapping Intervals", "Meeting Rooms",
                "Meeting Rooms II", "Meeting Rooms III", "Minimum Interval to Include Each Query"
            ],
            "Math & Geometry": [
                "Excel Sheet Column Title", "Greatest Common Divisor of Strings",
                "Insert Greatest Common Divisors in Linked List", "Transpose Matrix", "Rotate Image",
                "Spiral Matrix", "Set Matrix Zeroes", "Happy Number", "Plus One", "Roman to Integer",
                "Pow(x, n)", "Multiply Strings", "Detect Squares"
            ],
            "Bit Manipulation": [
                "Single Number", "Number of 1 Bits", "Counting Bits", "Add Binary", "Reverse Bits",
                "Missing Number", "Sum of Two Integers", "Reverse Integer", "Bitwise AND of Numbers Range",
                "Minimum Array End"
            ]
        }
        
        # Create a flat list of all problems with their categories
        self.all_problems = []
        for category, problems in self.problems.items():
            for problem in problems:
                self.all_problems.append((problem, category))

    def get_leetcode_url(self, problem_name):
        """Convert problem name to LeetCode URL format"""
        # Convert to URL format: "Two Sum" -> "two-sum"
        url_name = problem_name.lower().replace(" ", "-")
        # Handle special characters
        url_name = url_name.replace("'", "").replace(",", "").replace("(", "").replace(")", "")
        url_name = url_name.replace("&", "and").replace("/", "-").replace(":", "")
        return f"https://leetcode.com/problems/{url_name}/"

    @commands.command(name='leetcode', aliases=['lc', 'neetcode', 'randomproblem'], help='Get a random LeetCode problem from NeetCode 250.')
    async def random_leetcode(self, ctx, category: str = None):
        if category:
            # Search for category (case-insensitive, partial match)
            category_lower = category.lower()
            matching_categories = [cat for cat in self.problems.keys() if category_lower in cat.lower()]
            
            if not matching_categories:
                await ctx.send(f"❌ Category '{category}' not found. Use `!leetcode` to see all categories.")
                return
            
            # Use first matching category
            selected_category = matching_categories[0]
            problems = self.problems[selected_category]
            problem = random.choice(problems)
            problem_category = selected_category
        else:
            # Random problem from all categories
            problem, problem_category = random.choice(self.all_problems)
        
        # Get LeetCode URL
        leetcode_url = self.get_leetcode_url(problem)
        
        # Create embed
        embed = nextcord.Embed(
            title="💻 Random LeetCode Problem",
            description=f"**{problem}**",
            color=nextcord.Color.green()
        )
        
        embed.add_field(
            name="📚 Category",
            value=problem_category,
            inline=True
        )
        
        embed.add_field(
            name="🔗 LeetCode",
            value=f"[View Problem]({leetcode_url})",
            inline=True
        )
        
        embed.add_field(
            name="📖 NeetCode",
            value="[NeetCode 250](https://neetcode.io/practice)",
            inline=False
        )
        
        embed.set_footer(text="Practice makes perfect! 💪")
        
        await ctx.send(embed=embed)

    @commands.command(name='leetcodecategories', aliases=['lccategories', 'neetcodecats'], help='List all available LeetCode problem categories.')
    async def list_categories(self, ctx):
        embed = nextcord.Embed(
            title="📚 NeetCode 250 Categories",
            description="Available problem categories:",
            color=nextcord.Color.blue()
        )
        
        categories_text = "\n".join([f"• {cat} ({len(self.problems[cat])} problems)" for cat in self.problems.keys()])
        embed.add_field(
            name="Categories",
            value=categories_text,
            inline=False
        )
        
        embed.add_field(
            name="Usage",
            value="Use `!leetcode <category>` to get a random problem from a specific category.\nExample: `!leetcode arrays`",
            inline=False
        )
        
        embed.set_footer(text="Total: 250 problems across all categories")
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(LeetCode(bot))

