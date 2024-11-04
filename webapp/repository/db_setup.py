from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, text
from sqlalchemy.orm import sessionmaker

# Initialize SQLite database
engine = create_engine('sqlite:///example.db')
metadata = MetaData()
Session = sessionmaker(bind=engine)

# Define tables with descriptions based on the summary
epic = Table('Epic', metadata,
    Column('epic_id', Integer, primary_key=True, info={'description': 'Unique identifier for each epic'}),
    Column('epic_key', String(50), info={'description': 'Unique key representing the epic'}),
    Column('name', String(255), info={'description': 'Name of the epic'}),
    Column('description', String, info={'description': 'Detailed description of the epic'}),
    Column('status', String(50), info={'description': 'Current status of the epic, such as Open, In Progress, or Closed'}),
    Column('created_at', String, info={'description': 'Timestamp of when the epic was created'}),
    Column('updated_at', String, info={'description': 'Timestamp of the last update to the epic'}),
    info={'description': 'The **Epic** table contains data related to larger work items or projects, with each entry represented by `epic_id`, `epic_key`, `name`, `description`, and `status`. It also stores `created_at` and `updated_at` timestamps, indicating when the epic was created and last modified. This table can be used to analyze project-level information, track progress across multiple tasks related to an epic, and manage high-level objectives. Possible questions it can address include identifying active projects, tracking epics based on their status, or understanding the distribution of tasks under each epic'}
)

user = Table('User', metadata,
    Column('user_id', Integer, primary_key=True, info={'description': 'Unique identifier for each user'}),
    Column('username', String(50), info={'description': 'Unique username of the user'}),
    Column('email', String(255), unique=True, info={'description': 'Email address of the user, must be unique'}),
    Column('display_name', String(100), info={'description': 'Display name of the user'}),
    info={'description': 'The **User** table stores data on individuals involved in tasks or commits, identified by `user_id`, `username`, `email`, and `display_name`. It provides a reference point for assigning or attributing tasks, commits, and pull requests to specific users. This table can be used for user-based analyses, such as tracking user contributions, analyzing workload distribution among team members, and identifying active users.'}
)

jira_task = Table('JiraTask', metadata,
    Column('task_id', Integer, primary_key=True, info={'description': 'Unique identifier for each task'}),
    Column('task_key', String(50), info={'description': 'Unique key representing the task'}),
    Column('summary', String(255), info={'description': 'Short summary of the task'}),
    Column('description', String, info={'description': 'Detailed description of the task'}),
    Column('status', String(50), info={'description': 'Current status of the task, such as In Progress,In Review, Completed, or Closed'}),
    Column('created_at', String, info={'description': 'Timestamp of when the task was created'}),
    Column('updated_at', String, info={'description': 'Timestamp of the last update to the task'}),
    Column('author_id', Integer, ForeignKey('User.user_id'), info={'description': 'ID of the user who created the task'}),
    Column('owner_id', Integer, ForeignKey('User.user_id'), info={'description': 'ID of the user currently responsible for the task'}),
    Column('epic_id', Integer, ForeignKey('Epic.epic_id'), info={'description': 'ID of the epic this task is associated with'}),
    info={'description': 'The **JiraTask** table records individual tasks, identified by fields like `task_id`, `task_key`, `summary`, `description`, and `status`. It includes timestamps (`created_at`, `updated_at`) and links to users (`author_id` and `owner_id`) and epics (`epic_id`) for task context. This table can facilitate task management, author and owner tracking, and task distribution across various epics. Potential uses include tracking task completion rates, evaluating task ownership and assignments, and examining the evolution of tasks over time'}
)

task_status_history = Table('TaskStatusHistory', metadata,
    Column('id', Integer, primary_key=True, info={'description': 'Unique identifier for each status history record'}),
    Column('task_id', Integer, ForeignKey('JiraTask.task_id'), info={'description': 'ID of the task this status history is associated with'}),
    Column('status', String(50), info={'description': 'Status of the task at this point in time status can be Open or In Progress, In Review, or Completed'},),
    Column('entered_at', String, info={'description': 'Timestamp when the task entered this status'}),
    info={'description': 'The **TaskStatusHistory** table captures the historical statuses of tasks over time. For each `task_id`, it records entries for each status change, including `status`, `entered_at`. This allows analysis of the time each task spent in different statuses, which can be valuable for understanding bottlenecks, evaluating the efficiency of task workflows, and monitoring time spent in stages like review or testing'}
)

# Define GitBranch table for branch information
git_branch = Table('GitBranch', metadata,
    Column('branch_id', Integer, primary_key=True, info={'description': 'Unique identifier for each branch'}),
    Column('name', String(255), info={'description': 'Name of the branch'}),
    Column('task_id', Integer, ForeignKey('JiraTask.task_id')),
    info={'description': 'Table for storing branch information, linking branches to commits and pull requests.'}
)

commit = Table('Commit_Table', metadata,
    Column('commit_id', Integer, primary_key=True, info={'description': 'Unique identifier for each commit'}),
    Column('hash', String(40), info={'description': 'Unique hash of the commit'}),
    Column('message', String, info={'description': 'Commit message providing details about the change'}),
    Column('author_id', Integer, ForeignKey('User.user_id'), info={'description': 'ID of the user who made the commit'}),
    Column('timestamp', String, info={'description': 'Timestamp of when the commit was made'}),
    Column('branch_id', Integer, ForeignKey('GitBranch.branch_id'), info={'description': 'ID of the branch this commit is associated with'}),
    info={'description': 'The **Commit** table logs individual code commits, capturing `commit_id`, `hash`, `message`, `author_id`, `timestamp`, and `branch_id`. Each entry links a commit to a specific user and branch, allowing tracking of code contributions and linking of commits to tasks through branches. This table enables tracking the frequency of commits, examining commit activity over time, and associating code changes with specific tasks and branches'}
)

pull_request = Table('PullRequest', metadata,
    Column('pr_id', Integer, primary_key=True, info={'description': 'Unique identifier for each pull request'}),
    Column('number', Integer, info={'description': 'Number of the pull request'}),
    Column('title', String(255), info={'description': 'Title of the pull request'}),
    Column('description', String, info={'description': 'Detailed description of the pull request'}),
    Column('status', String(50), info={'description': 'Current status of the pull request, such as Open, Merged, or Closed'}),
    Column('created_at', String, info={'description': 'Timestamp of when the pull request was created'}),
    Column('merged_at', String, info={'description': 'Timestamp of when the pull request was merged, if applicable'}),
    Column('author_id', Integer, ForeignKey('User.user_id'), info={'description': 'ID of the user who created the pull request'}),
    Column('branch_id', Integer, ForeignKey('GitBranch.branch_id'), info={'description': 'ID of the branch this pull request is associated with'}),
    info={'description': 'The **PullRequest** table contains information about code pull requests, including `pr_id`, `number`, `title`, `description`, `status`, and `created_at` and `merged_at` timestamps. Each pull request also links to an author and branch. This table can be used to evaluate pull request activity, measure the time taken for reviews and merges, and analyze the association of pull requests with specific tasks'}
)

# Create tables in the SQLite database
metadata.drop_all(engine)
metadata.create_all(engine)


def insert_dummy_data():
    session = Session()
    with session.begin():
        # Insert additional Users
        session.execute(user.insert(), [
            {'user_id': 1, 'username': 'Alice', 'email': 'alice@example.com', 'display_name': 'Alice'},
            {'user_id': 2, 'username': 'Bob', 'email': 'bob@example.com', 'display_name': 'Bob'},
            {'user_id': 3, 'username': 'Charlie', 'email': 'charlie@example.com', 'display_name': 'Charlie'},
            {'user_id': 4, 'username': 'Dave', 'email': 'dave@example.com', 'display_name': 'Dave'},
            {'user_id': 5, 'username': 'Eve', 'email': 'eve@example.com', 'display_name': 'Eve'}
        ])

        # Insert Epics
        session.execute(epic.insert(), [
            {'epic_id': 1, 'epic_key': 'EPIC-1', 'name': 'Epic One', 'description': 'First epic', 'status': 'Open',
             'created_at': '2024-11-01', 'updated_at': '2024-11-02'},
            {'epic_id': 2, 'epic_key': 'EPIC-2', 'name': 'Epic Two', 'description': 'Second epic',
             'status': 'In Progress', 'created_at': '2024-11-03', 'updated_at': '2024-11-04'}
        ])

        # Insert JiraTasks
        session.execute(jira_task.insert(), [
            {'task_id': 1, 'task_key': 'TASK-1', 'summary': 'Task One', 'description': 'First task', 'status': 'Completed', 'created_at': '2024-11-01', 'updated_at': '2024-11-05', 'author_id': 1, 'owner_id': 2, 'epic_id': 1},
            {'task_id': 2, 'task_key': 'TASK-2', 'summary': 'Task Two', 'description': 'Second task', 'status': 'Completed', 'created_at': '2024-11-03', 'updated_at': '2024-11-07', 'author_id': 2, 'owner_id': 3, 'epic_id': 1},
            {'task_id': 3, 'task_key': 'TASK-3', 'summary': 'Task Three', 'description': 'Third task', 'status': 'In Review', 'created_at': '2024-11-05', 'updated_at': '2024-11-06', 'author_id': 3, 'owner_id': 4, 'epic_id': 1},
            {'task_id': 4, 'task_key': 'TASK-4', 'summary': 'Task Four', 'description': 'Fourth task', 'status': 'Open', 'created_at': '2024-11-07', 'updated_at': '2024-11-08', 'author_id': 4, 'owner_id': 1, 'epic_id': 2},
            {'task_id': 5, 'task_key': 'TASK-5', 'summary': 'Task Five', 'description': 'Fifth task', 'status': 'In Progress', 'created_at': '2024-11-09', 'updated_at': '2024-11-10', 'author_id': 5, 'owner_id': 2, 'epic_id': 2},
            {'task_id': 6, 'task_key': 'TASK-6', 'summary': 'Task Six', 'description': 'Sixth task', 'status': 'Completed', 'created_at': '2024-11-11', 'updated_at': '2024-11-17', 'author_id': 1, 'owner_id': 3, 'epic_id': 2},
            {'task_id': 7, 'task_key': 'TASK-7', 'summary': 'Task Seven', 'description': 'Seventh task', 'status': 'Completed', 'created_at': '2024-11-13', 'updated_at': '2024-11-20', 'author_id': 2, 'owner_id': 4, 'epic_id': 2}
        ])

        # Insert TaskStatusHistory records, including tasks with full life cycles
        session.execute(task_status_history.insert(), [
            # Task 1: Complete life cycle
            {'id': 1, 'task_id': 1, 'status': 'Open', 'entered_at': '2024-11-01T09:00:00'},
            {'id': 2, 'task_id': 1, 'status': 'In Progress', 'entered_at': '2024-11-01T10:00:00'},
            {'id': 3, 'task_id': 1, 'status': 'In Review', 'entered_at': '2024-11-03T15:00:00'},
            {'id': 4, 'task_id': 1, 'status': 'Completed', 'entered_at': '2024-11-04T12:00:00'},

            # Task 2: Complete life cycle
            {'id': 5, 'task_id': 2, 'status': 'Open', 'entered_at': '2024-11-03T10:00:00'},
            {'id': 6, 'task_id': 2, 'status': 'In Progress', 'entered_at': '2024-11-04T09:00:00'},
            {'id': 7, 'task_id': 2, 'status': 'In Review', 'entered_at': '2024-11-05T16:00:00'},
            {'id': 8, 'task_id': 2, 'status': 'Completed', 'entered_at': '2024-11-06T11:00:00'},

            # Task 3: Partial life cycle (In Review only)
            {'id': 9, 'task_id': 3, 'status': 'In Review', 'entered_at': '2024-11-05T11:00:00'},

            # Task 4: Open status only
            {'id': 10, 'task_id': 4, 'status': 'Open', 'entered_at': '2024-11-07T08:00:00'},

            # Task 5: In Progress status only
            {'id': 11, 'task_id': 5, 'status': 'In Progress', 'entered_at': '2024-11-09T09:00:00'},

            # Task 6: Complete life cycle
            {'id': 12, 'task_id': 6, 'status': 'Open', 'entered_at': '2024-11-11T14:00:00'},
            {'id': 13, 'task_id': 6, 'status': 'In Progress', 'entered_at': '2024-11-12T09:00:00'},
            {'id': 14, 'task_id': 6, 'status': 'In Review', 'entered_at': '2024-11-14T17:00:00'},
            {'id': 15, 'task_id': 6, 'status': 'Completed', 'entered_at': '2024-11-16T18:00:00'},

            # Task 7: Complete life cycle
            {'id': 16, 'task_id': 7, 'status': 'Open', 'entered_at': '2024-11-13T10:00:00'},
            {'id': 17, 'task_id': 7, 'status': 'In Progress', 'entered_at': '2024-11-14T11:00:00'},
            {'id': 18, 'task_id': 7, 'status': 'In Review', 'entered_at': '2024-11-16T15:00:00'},
            {'id': 19, 'task_id': 7, 'status': 'Completed', 'entered_at': '2024-11-18T12:00:00'}
        ])

        # Insert GitBranches linked to tasks
        session.execute(git_branch.insert(), [
            {'branch_id': 1, 'name': 'feature/task-1', 'task_id': 1},
            {'branch_id': 2, 'name': 'feature/task-2', 'task_id': 2},
            {'branch_id': 3, 'name': 'feature/task-2-update', 'task_id': 2},
            {'branch_id': 4, 'name': 'feature/task-3', 'task_id': 3},
            {'branch_id': 5, 'name': 'feature/task-6', 'task_id': 6}
        ])

        # Insert Commits
        session.execute(commit.insert(), [
            # Commits for Task 1 by Alice
            {'commit_id': 1, 'hash': 'abc123', 'message': 'Initial commit for Task 1', 'author_id': 1,
             'timestamp': '2024-11-01T10:00:00', 'branch_id': 1},
            {'commit_id': 2, 'hash': 'bcd234', 'message': 'Update Task 1', 'author_id': 1,
             'timestamp': '2024-11-01T12:00:00', 'branch_id': 1},

            # Commits for Task 2 by Bob
            {'commit_id': 3, 'hash': 'def456', 'message': 'Work on Task 2', 'author_id': 2,
             'timestamp': '2024-11-03T12:00:00', 'branch_id': 2},
            {'commit_id': 4, 'hash': 'efg567', 'message': 'More work on Task 2', 'author_id': 2,
             'timestamp': '2024-11-04T14:00:00', 'branch_id': 2},
            {'commit_id': 5, 'hash': 'fgh678', 'message': 'Finalizing Task 2', 'author_id': 2,
             'timestamp': '2024-11-05T16:00:00', 'branch_id': 2},

            # Commits for Task 2 on another branch by Bob
            {'commit_id': 6, 'hash': 'ghi789', 'message': 'Hotfix for Task 2', 'author_id': 2,
             'timestamp': '2024-11-06T10:00:00', 'branch_id': 3},

            # Commits for Task 3 by Charlie
            {'commit_id': 7, 'hash': 'hij890', 'message': 'Initial commit for Task 3', 'author_id': 3,
             'timestamp': '2024-11-05T15:00:00', 'branch_id': 4},
            {'commit_id': 8, 'hash': 'ijk901', 'message': 'Update Task 3', 'author_id': 3,
             'timestamp': '2024-11-06T17:00:00', 'branch_id': 4},

            # Commits for Task 6 by Alice
            {'commit_id': 9, 'hash': 'jkl012', 'message': 'Start work on Task 6', 'author_id': 1,
             'timestamp': '2024-11-11T15:00:00', 'branch_id': 5}
        ])

        # Insert PullRequests
        session.execute(pull_request.insert(), [
            # Pull Requests for Task 1
            {'pr_id': 1, 'number': 101, 'title': 'PR for Task 1', 'description': 'Pull request for Task 1',
             'status': 'Merged', 'created_at': '2024-11-01T13:00:00', 'merged_at': '2024-11-02T10:00:00',
             'author_id': 1, 'branch_id': 1},

            # Pull Requests for Task 2
            {'pr_id': 2, 'number': 102, 'title': 'First PR for Task 2', 'description': 'Pull request for Task 2',
             'status': 'Merged', 'created_at': '2024-11-03T15:00:00', 'merged_at': '2024-11-05T13:00:00',
             'author_id': 2, 'branch_id': 2},
            {'pr_id': 3, 'number': 103, 'title': 'Second PR for Task 2',
             'description': 'Second pull request for Task 2', 'status': 'Merged', 'created_at': '2024-11-06T11:00:00',
             'merged_at': '2024-11-07T14:00:00', 'author_id': 2, 'branch_id': 3},

            # Pull Request for Task 3
            {'pr_id': 4, 'number': 104, 'title': 'PR for Task 3', 'description': 'Pull request for Task 3',
             'status': 'Open', 'created_at': '2024-11-07T18:00:00', 'merged_at': None, 'author_id': 3, 'branch_id': 4},

            # Pull Request for Task 6
            {'pr_id': 5, 'number': 105, 'title': 'PR for Task 6', 'description': 'Pull request for Task 6',
             'status': 'Merged', 'created_at': '2024-11-12T10:00:00', 'merged_at': '2024-11-16T17:00:00',
             'author_id': 1, 'branch_id': 5}
        ])

    session.commit()

insert_dummy_data()


# Function to get schema descriptions
def get_schema_descriptions():
    """Extract schema descriptions from the database with custom descriptions."""
    schemas = []
    for table_name, table in metadata.tables.items():
        # Get table description
        table_description = table.info.get('description', 'No description available')

        # Extract column descriptions
        columns = []
        for column in table.columns:
            column_description = column.info.get('description', 'No description available')
            column_info = {
                "column_name": column.name,
                "column_type": str(column.type),
                "is_primary_key": column.primary_key,
                "is_unique": column.unique,
                "description": column_description
            }
            columns.append(column_info)

        # Organize table schema
        schema = {
            "table_name": table_name,
            "table_description": table_description,
            "columns": columns
        }
        schemas.append(schema)
    return schemas


