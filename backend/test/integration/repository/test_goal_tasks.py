import datetime

from backend.models.models import (
    Goals,
    GoalsStatusEnum,
    GoalsTasks,
    GoalsTasksStatusEnum,
    Users,
)
from backend.repository.repository import (
    GoalRepository,
    GoalTaskRepository,
    GoalTaskNotFound,
    StatusUnchangedError,
    UserRepository,
)
from backend.test.integration.test_base import TestBase


class TestGoalTaskRepository(TestBase):
    def setUp(self):
        super(TestGoalTaskRepository, self).setUp()
        user_data = Users(
            username="sasasasasa",
            hashed_password="abcd",
            email="sasasasa@example.com",
        )
        user_repository = UserRepository()
        self.user = user_repository.register_user(self.db, user_data, commit=True)
        self.goal_data = Goals(
            user_id=self.user.user_id,
            goal_name="TOEIC800点取得",
            start_day=datetime.date(2030, 10, 15),
            target_day=datetime.date(2030, 10, 22),
            status=GoalsStatusEnum.Unachieved.value,
            status_against_goal="TOEIC模擬テストで400点を取得",
            weekday_available_time=60,
            weekends_available_time=90,
            total_estimated_time=1000,
            task_creation_rule="リーディングに重点をおいてタスク生成したい",
        )
        goal_repository = GoalRepository()
        self.goal = goal_repository.register_goal(self.db, self.goal_data, commit=True)
        self.goal_task_repository = GoalTaskRepository()

    def _task(
        self,
        name="英単語帳を暗記",
        status=GoalsTasksStatusEnum.Todo.value,
        order_num=None,
        goal_id=None,
    ):
        return GoalsTasks(
            goal_id=goal_id or self.goal.goal_id,
            goal_task_name=name,
            deadline=datetime.date(2030, 10, 15),
            estimated_time=180,
            goal_task_status=status,
            order_num=order_num,
        )

    def _register_two_tasks(self):
        tasks = [
            self._task(name="task1", order_num=1),
            self._task(name="task2", order_num=2),
        ]
        return self.goal_task_repository.register_goal_task(self.db, tasks, commit=True)

    def _create_another_goal(self):
        another_user = UserRepository().register_user(
            self.db,
            Users(
                username="another_user",
                hashed_password="abcd",
                email="another@example.com",
            ),
            commit=True,
        )
        another_goal = Goals(
            user_id=another_user.user_id,
            goal_name="簿記2級合格",
            start_day=datetime.date(2030, 11, 1),
            target_day=datetime.date(2030, 11, 30),
            status=GoalsStatusEnum.Achieved.value,
            status_against_goal="現在3級レベル",
            weekday_available_time=60,
            weekends_available_time=120,
            total_estimated_time=500,
            task_creation_rule="問題集中心",
        )
        goal_repository = GoalRepository()
        return goal_repository.register_goal(self.db, another_goal, commit=True)

    def test_get_goal_task_by_goal_task_id_from_db(self):
        task = self.goal_task_repository.register_goal_task(
            self.db, [self._task()], commit=True
        )[0]

        fetched = self.goal_task_repository.get_goal_task_by_goal_task_id_from_db(
            self.db, task.goal_task_id
        )

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.goal_task_id, task.goal_task_id)

    def test_get_goal_task_by_goal_id_returns_first_task(self):
        self._register_two_tasks()

        fetched = self.goal_task_repository.get_goal_task_by_goal_id(
            self.db, self.goal.goal_id
        )

        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.goal_id, self.goal.goal_id)

    def test_fetch_goal_tasks_by_goal_id_from_db_returns_ordered_tasks(self):
        tasks = [
            self._task(name="task3", order_num=3),
            self._task(name="task1", order_num=1),
            self._task(name="task2", order_num=2),
        ]
        self.goal_task_repository.register_goal_task(self.db, tasks, commit=True)

        fetched = self.goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            self.db, self.goal.goal_id
        )

        self.assertEqual([task.order_num for task in fetched], [1, 2, 3])

    def test_register_goal_task_assigns_order_when_order_num_is_none(self):
        tasks = [
            self._task(name="task1", order_num=None),
            self._task(name="task2", order_num=None),
        ]

        registered = self.goal_task_repository.register_goal_task(
            self.db, tasks, commit=True
        )

        self.assertEqual([task.order_num for task in registered], [1, 2])

    def test_delete_goal_task_from_db(self):
        task = self.goal_task_repository.register_goal_task(
            self.db, [self._task()], commit=True
        )[0]

        self.goal_task_repository.delete_goal_task_from_db(self.db, task)

        result = (
            self.db.query(GoalsTasks).filter_by(goal_task_id=task.goal_task_id).first()
        )
        self.assertIsNone(result, "達成目標タスクはデータベースから消去されていません")

    def test_replace_goal_tasks_from_db_replaces_all_tasks(self):
        self._register_two_tasks()
        new_tasks = [
            self._task(name="new1", order_num=None),
            self._task(name="new2", order_num=None),
            self._task(name="new3", order_num=None),
        ]

        replaced = self.goal_task_repository.replace_goal_tasks_from_db(
            self.db, self.goal.goal_id, new_tasks, commit=True
        )

        fetched = self.goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            self.db, self.goal.goal_id
        )
        self.assertEqual(len(replaced), 3)
        self.assertEqual(len(fetched), 3)
        self.assertEqual(
            [task.goal_task_name for task in fetched], ["new1", "new2", "new3"]
        )
        self.assertEqual([task.order_num for task in fetched], [1, 2, 3])

    def test_replace_goal_tasks_from_db_works_when_existing_is_empty(self):
        new_tasks = [
            self._task(name="new1", order_num=None),
            self._task(name="new2", order_num=None),
        ]

        replaced = self.goal_task_repository.replace_goal_tasks_from_db(
            self.db, self.goal.goal_id, new_tasks, commit=True
        )

        fetched = self.goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            self.db, self.goal.goal_id
        )
        self.assertEqual(len(replaced), 2)
        self.assertEqual([task.goal_task_name for task in fetched], ["new1", "new2"])
        self.assertEqual([task.order_num for task in fetched], [1, 2])

    def test_update_goal_task_status_and_order_from_db(self):
        task = self.goal_task_repository.register_goal_task(
            self.db,
            [self._task(status="未着手", order_num=1)],
            commit=True,
        )[0]

        updated = self.goal_task_repository.update_goal_task_status_and_order_from_db(
            self.db,
            task.goal_task_id,
            GoalsTasksStatusEnum.Completed,
            3,
            commit=True,
        )

        self.assertEqual(updated.goal_task_status, GoalsTasksStatusEnum.Completed.value)
        self.assertEqual(updated.order_num, 3)

    def test_update_goal_task_status_and_order_from_db_not_found(self):
        with self.assertRaises(GoalTaskNotFound):
            self.goal_task_repository.update_goal_task_status_and_order_from_db(
                self.db,
                999999,
                GoalsTasksStatusEnum.Completed,
                1,
                commit=True,
            )

    def test_update_goal_task_status_and_order_from_db_same_status_raises_error(self):
        task = self.goal_task_repository.register_goal_task(
            self.db,
            [self._task(status="作業中", order_num=1)],
            commit=True,
        )[0]

        with self.assertRaises(StatusUnchangedError):
            self.goal_task_repository.update_goal_task_status_and_order_from_db(
                self.db,
                task.goal_task_id,
                GoalsTasksStatusEnum.InProgress,
                2,
                commit=True,
            )

    def test_update_goal_task_order_from_db(self):
        task1, task2 = self._register_two_tasks()

        self.goal_task_repository.update_goal_task_order_from_db(
            self.db,
            from_goal_task_id=task1.goal_task_id,
            to_goal_task_id=task2.goal_task_id,
            commit=True,
        )

        fetched = self.goal_task_repository.fetch_goal_tasks_by_goal_id_from_db(
            self.db, self.goal.goal_id
        )
        self.assertEqual([task.goal_task_name for task in fetched], ["task2", "task1"])
        self.assertEqual([task.order_num for task in fetched], [1, 2])

    def test_update_goal_task_order_from_db_same_position_raises_error(self):
        task = self.goal_task_repository.register_goal_task(
            self.db, [self._task(order_num=1)], commit=True
        )[0]

        with self.assertRaises(StatusUnchangedError):
            self.goal_task_repository.update_goal_task_order_from_db(
                self.db,
                from_goal_task_id=task.goal_task_id,
                to_goal_task_id=task.goal_task_id,
                commit=True,
            )

    def test_update_goal_task_order_from_db_with_different_goals_raises_value_error(
        self,
    ):
        task = self.goal_task_repository.register_goal_task(
            self.db, [self._task(order_num=1)], commit=True
        )[0]
        another_goal = self._create_another_goal()
        another_task = self.goal_task_repository.register_goal_task(
            self.db,
            [self._task(name="another", order_num=1, goal_id=another_goal.goal_id)],
            commit=True,
        )[0]

        with self.assertRaises(ValueError):
            self.goal_task_repository.update_goal_task_order_from_db(
                self.db,
                from_goal_task_id=task.goal_task_id,
                to_goal_task_id=another_task.goal_task_id,
                commit=True,
            )

    def test_update_goal_task_from_db(self):
        task = self.goal_task_repository.register_goal_task(
            self.db, [self._task(name="before")], commit=True
        )[0]

        updated = self.goal_task_repository.update_goal_task_from_db(
            self.db,
            goal_task_id=task.goal_task_id,
            goal_task_name="after",
            deadline=datetime.date(2030, 10, 20),
            estimated_time=90,
            commit=True,
        )

        self.assertEqual(updated.goal_task_name, "after")
        self.assertEqual(updated.deadline, datetime.date(2030, 10, 20))
        self.assertEqual(updated.estimated_time, 90)

    def test_update_goal_task_from_db_not_found(self):
        with self.assertRaises(GoalTaskNotFound):
            self.goal_task_repository.update_goal_task_from_db(
                self.db,
                goal_task_id=999999,
                goal_task_name="after",
                deadline=datetime.date(2030, 10, 20),
                estimated_time=90,
                commit=True,
            )
